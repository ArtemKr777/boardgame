import os
import django
import pandas as pd
import numpy as np
from collections import Counter

# Настройка Django окружения
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from games.models import Game
from django.contrib.auth.models import User
from users.models import Profile, OwnedGame, PlayedGame, PlayerResult


# =====================================================
# 1. ДАННЫЕ ОБ ИГРАХ (GAMES DATAFRAME)
# =====================================================

def get_games_dataframe():
    """Извлекает все игры с их характеристиками"""
    games = Game.objects.all()

    data = []
    for game in games:
        # Парсим тематики и категории в списки
        themes_list = [t.strip() for t in game.thematics.split(',') if t.strip()] if game.thematics else []
        categories_list = [c.strip() for c in game.categories.split(',') if c.strip()] if game.categories else []

        row = {
            'game_id': game.id,
            'name': game.name,
            'min_players': game.min_players,
            'max_players': game.max_players,
            'avg_players': (game.min_players + game.max_players) / 2,
            'min_duration': game.min_duration or 0,
            'max_duration': game.max_duration or 0,
            'avg_duration': ((game.min_duration or 0) + (game.max_duration or 0)) / 2,
            'min_age': game.min_age or 0,
            'max_age': game.max_age or 0,
            'avg_age': ((game.min_age or 0) + (game.max_age or 0)) / 2,
            'thematics_raw': game.thematics,
            'categories_raw': game.categories,
            'thematics_list': themes_list,
            'categories_list': categories_list,
            'thematics_count': len(themes_list),
            'categories_count': len(categories_list),
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df


# =====================================================
# 2. ДАННЫЕ О ПОЛЬЗОВАТЕЛЯХ (USERS DATAFRAME)
# =====================================================

def get_users_dataframe():
    """Извлекает всех пользователей с их профилями"""
    users = User.objects.all()

    data = []
    for user in users:
        profile = Profile.objects.filter(user=user).first()

        row = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name or '',
            'date_joined': user.date_joined,
            'age': profile.age if profile and profile.age else 0,
            'city': profile.city if profile and profile.city else '',
            'has_phone': 1 if profile and profile.phone else 0,
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df


# =====================================================
# 3. КОЛЛЕКЦИЯ ИГР ПОЛЬЗОВАТЕЛЕЙ (OWNED GAMES DATAFRAME)
# =====================================================

def get_owned_games_dataframe():
    """Извлекает, какие игры есть у пользователей в коллекции"""
    owned = OwnedGame.objects.select_related('user', 'game').all()

    data = []
    for own in owned:
        row = {
            'user_id': own.user.id,
            'game_id': own.game.id,
            'game_name': own.game.name,
            'added_at': own.added_at,
        }
        data.append(row)

    df = pd.DataFrame(data)
    return df


# =====================================================
# 4. ИСТОРИЯ ИГР ПОЛЬЗОВАТЕЛЕЙ (HISTORY DATAFRAME)
# =====================================================

def get_user_history_dataframe():
    """
    Извлекает все сыгранные партии с результатами участников.
    Возвращает DataFrame, где каждая строка = одна партия для одного игрока.
    """
    played_games = PlayedGame.objects.select_related('user', 'game').prefetch_related('results').all()

    data = []
    for played in played_games:
        # Для каждого участника в партии создаём отдельную строку
        results = PlayerResult.objects.filter(played_game=played).select_related('player')

        if results.exists():
            for result in results:
                row = {
                    'played_game_id': played.id,
                    'game_id': played.game.id,
                    'game_name': played.game.name,
                    'user_id': result.player.id,  # участник
                    'recorder_id': played.user.id,  # кто записал партию
                    'play_date': played.play_date,
                    'duration_minutes': played.duration_minutes or 0,
                    'place': result.place,
                    'score': result.score or 0,
                    'comment': played.comment or '',
                }
                data.append(row)
        else:
            # Если нет результатов (старые данные), создаём запись только для записавшего
            row = {
                'played_game_id': played.id,
                'game_id': played.game.id,
                'game_name': played.game.name,
                'user_id': played.user.id,
                'recorder_id': played.user.id,
                'play_date': played.play_date,
                'duration_minutes': played.duration_minutes or 0,
                'place': 1,
                'score': 0,
                'comment': played.comment or '',
            }
            data.append(row)

    df = pd.DataFrame(data)

    # Добавляем вычисленный рейтинг: место → рейтинг (1 место = 5, 2 = 4, ...)
    if not df.empty:
        df['rating'] = df['place'].apply(lambda x: max(1, 6 - x) if x <= 5 else 1)

    return df


# =====================================================
# 5. МАТРИЦА ПОЛЬЗОВАТЕЛЬ-ИГРА (USER-GAME MATRIX)
# =====================================================

def get_user_game_matrix(history_df=None):
    """
    Создаёт матрицу user_id × game_id, где значение = рейтинг.
    Для коллаборативной фильтрации.
    """
    if history_df is None:
        history_df = get_user_history_dataframe()

    if history_df.empty:
        return pd.DataFrame()

    # Берём только нужные колонки и убираем дубликаты (если один пользователь играл в одну игру несколько раз)
    # Берём средний рейтинг для каждой пары user-game
    matrix_data = history_df.groupby(['user_id', 'game_id'])['rating'].mean().reset_index()

    # Создаём матрицу
    user_game_matrix = matrix_data.pivot(index='user_id', columns='game_id', values='rating')
    user_game_matrix = user_game_matrix.fillna(0)

    return user_game_matrix


# =====================================================
# 6. ПРИЗНАКИ ПОЛЬЗОВАТЕЛЕЙ ДЛЯ ML (USER FEATURES)
# =====================================================

def get_user_ml_features(history_df=None, users_df=None, owned_df=None):
    """
    Создаёт набор признаков для каждого пользователя:
    - возраст
    - количество сыгранных партий
    - средний рейтинг
    - любимые тематики (TOP-3)
    - средняя длительность игры
    - разнообразие игр (уникальные игры)
    - количество игр в коллекции
    """
    if users_df is None:
        users_df = get_users_dataframe()

    if history_df is None:
        history_df = get_user_history_dataframe()

    if owned_df is None:
        owned_df = get_owned_games_dataframe()

    features = []

    for _, user_row in users_df.iterrows():
        user_id = user_row['user_id']

        # История пользователя
        user_history = history_df[history_df['user_id'] == user_id]

        # Коллекция пользователя
        user_owned = owned_df[owned_df['user_id'] == user_id]

        # Агрегированные признаки
        total_games = len(user_history)
        unique_games = user_history['game_id'].nunique() if not user_history.empty else 0
        avg_rating = user_history['rating'].mean() if not user_history.empty else 0
        avg_duration = user_history['duration_minutes'].mean() if not user_history.empty else 0

        # Любимые тематики (из сыгранных игр)
        theme_counter = Counter()
        if not user_history.empty:
            game_ids = user_history['game_id'].unique()
            games = Game.objects.filter(id__in=game_ids)
            for game in games:
                if game.thematics:
                    for theme in game.thematics.split(','):
                        theme_counter[theme.strip()] += 1
        top_themes = [theme for theme, _ in theme_counter.most_common(3)]

        feature_row = {
            'user_id': user_id,
            'age': user_row['age'],
            'city': user_row['city'],
            'total_games_played': total_games,
            'unique_games_played': unique_games,
            'avg_rating': avg_rating,
            'avg_duration_minutes': avg_duration,
            'games_in_collection': len(user_owned),
            'top_theme_1': top_themes[0] if len(top_themes) > 0 else '',
            'top_theme_2': top_themes[1] if len(top_themes) > 1 else '',
            'top_theme_3': top_themes[2] if len(top_themes) > 2 else '',
            'has_history': 1 if total_games > 0 else 0,
        }
        features.append(feature_row)

    df = pd.DataFrame(features)
    return df


# =====================================================
# 7. ПРИЗНАКИ ИГР ДЛЯ ML (GAME FEATURES)
# =====================================================

def get_game_ml_features(games_df=None):
    """Создаёт признаки для игр для контентной фильтрации"""
    if games_df is None:
        games_df = get_games_dataframe()

    # One-hot encoding для топ-категорий
    all_categories = []
    for cat_list in games_df['categories_list']:
        all_categories.extend(cat_list)

    top_categories = [cat for cat, count in Counter(all_categories).most_common(15)]

    # Создаём колонки для топ-категорий
    for category in top_categories:
        games_df[f'cat_{category.replace(" ", "_")}'] = games_df['categories_list'].apply(
            lambda x: 1 if category in x else 0
        )

    # One-hot encoding для топ-тематик
    all_themes = []
    for theme_list in games_df['thematics_list']:
        all_themes.extend(theme_list)

    top_themes = [theme for theme, count in Counter(all_themes).most_common(10)]

    for theme in top_themes:
        games_df[f'theme_{theme.replace(" ", "_")}'] = games_df['thematics_list'].apply(
            lambda x: 1 if theme in x else 0
        )

    # Выбираем колонки для ML
    feature_cols = [
        'game_id', 'min_players', 'max_players', 'avg_players',
        'min_duration', 'max_duration', 'avg_duration',
        'min_age', 'max_age', 'avg_age',
        'thematics_count', 'categories_count'
    ]

    # Добавляем one-hot колонки
    feature_cols.extend([f'cat_{cat.replace(" ", "_")}' for cat in top_categories])
    feature_cols.extend([f'theme_{theme.replace(" ", "_")}' for theme in top_themes])

    return games_df[feature_cols]


# =====================================================
# 8. ГЛАВНАЯ ФУНКЦИЯ ДЛЯ СБОРА ВСЕХ ДАННЫХ
# =====================================================

def collect_all_ml_data():
    """
    Собирает все DataFrames для ML в одном месте.
    Возвращает словарь с DataFrames.
    """
    print("📊 Извлечение данных для ML-модуля...")

    print("  - Загрузка игр...")
    games_df = get_games_dataframe()
    print(f"    ✅ Загружено {len(games_df)} игр")

    print("  - Загрузка пользователей...")
    users_df = get_users_dataframe()
    print(f"    ✅ Загружено {len(users_df)} пользователей")

    print("  - Загрузка коллекций...")
    owned_df = get_owned_games_dataframe()
    print(f"    ✅ Загружено {len(owned_df)} записей о коллекциях")

    print("  - Загрузка истории игр...")
    history_df = get_user_history_dataframe()
    print(f"    ✅ Загружено {len(history_df)} записей об играх")

    print("  - Создание матрицы пользователь-игра...")
    user_game_matrix = get_user_game_matrix(history_df)
    print(f"    ✅ Матрица {user_game_matrix.shape[0]} × {user_game_matrix.shape[1]}")

    print("  - Подготовка признаков пользователей...")
    user_features_df = get_user_ml_features(history_df, users_df, owned_df)
    print(f"    ✅ {len(user_features_df)} пользователей с признаками")

    print("  - Подготовка признаков игр...")
    game_features_df = get_game_ml_features(games_df)
    print(f"    ✅ {len(game_features_df)} игр с {len(game_features_df.columns) - 1} признаками")

    return {
        'games': games_df,
        'users': users_df,
        'owned_games': owned_df,
        'history': history_df,
        'user_game_matrix': user_game_matrix,
        'user_features': user_features_df,
        'game_features': game_features_df,
    }


# =====================================================
# 9. СОХРАНЕНИЕ В CSV (опционально)
# =====================================================

def save_all_to_csv(output_dir='ml_data'):
    """Сохраняет все DataFrames в CSV файлы для дальнейшего использования"""
    import os

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    data = collect_all_ml_data()

    for name, df in data.items():
        if isinstance(df, pd.DataFrame) and not df.empty:
            filepath = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"💾 Сохранено: {filepath} ({len(df)} строк)")
        else:
            print(f"⚠️ Пропущен {name} — DataFrame пуст")

    print("\n✅ Все данные сохранены!")


# =====================================================
# 10. ЗАПУСК (если скрипт запущен напрямую)
# =====================================================

if __name__ == '__main__':
    # Вариант 1: просто собрать данные и вывести статистику
    data = collect_all_ml_data()

    print("\n" + "=" * 50)
    print("📊 СТАТИСТИКА ДАННЫХ ДЛЯ ML")
    print("=" * 50)
    print(f"Игр в каталоге: {len(data['games'])}")
    print(f"Пользователей: {len(data['users'])}")
    print(f"Записей в коллекциях: {len(data['owned_games'])}")
    print(f"Сыгранных партий (записей): {len(data['history'])}")
    print(
        f"Матрица user-game: {data['user_game_matrix'].shape[0]} пользователей × {data['user_game_matrix'].shape[1]} игр")
    print(
        f"Плотность матрицы: {(data['user_game_matrix'] > 0).sum().sum() / (data['user_game_matrix'].shape[0] * data['user_game_matrix'].shape[1]) * 100:.2f}%")

    # Вариант 2: сохранить в CSV (раскомментировать при необходимости)
    # save_all_to_csv()
    # Показать первые 5 строк каждого DataFrame
    print("\n" + "=" * 50)
    print("📋 ПРИМЕРЫ ДАННЫХ")
    print("=" * 50)

    print("\n1. Игры (первые 3):")
    print(data['games'][['game_id', 'name', 'min_players', 'max_players', 'avg_duration']].head(3).to_string())

    print("\n2. Пользователи:")
    print(data['users'][['user_id', 'username', 'age', 'city']].to_string())

    print("\n3. История игр (сыгранные партии):")
    print(data['history'][['user_id', 'game_name', 'place', 'rating', 'duration_minutes']].to_string())

    print("\n4. Матрица пользователь-игра:")
    print(data['user_game_matrix'].to_string())

    print("\n5. Признаки пользователей:")
    print(data['user_features'].to_string())

    print("\n6. Признаки игр (первые 3 игры, основные колонки):")
    game_cols = ['game_id', 'min_players', 'avg_duration', 'min_age', 'thematics_count', 'categories_count']
    print(data['game_features'][game_cols].head(3).to_string())

    # Сохраняем все данные в CSV файлы
    print("\n" + "=" * 50)
    print("💾 СОХРАНЕНИЕ ДАННЫХ В CSV")
    print("=" * 50)

    import os

    output_dir = 'ml_data'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for name, df in data.items():
        if isinstance(df, pd.DataFrame) and not df.empty:
            filepath = os.path.join(output_dir, f'{name}.csv')
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            print(f"✅ {name}.csv ({len(df)} строк)")
        else:
            print(f"⚠️ {name} — пустой DataFrame")

    print(f"\n📁 Все файлы сохранены в папку: {os.path.abspath(output_dir)}")