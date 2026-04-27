from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Game


@login_required
def game_list(request):
    games = Game.objects.all()

    # 1. Поиск по названию (регистронезависимый через LOWER)
    name_filter = request.GET.get('name', '').strip()
    if name_filter:
        # Приводим поисковый запрос и название игры к нижнему регистру
        games = games.filter(name__iregex=rf'.*{name_filter}.*')
        # Альтернативный способ, если iregex не работает:
        # games = [g for g in games if name_filter.lower() in g.name.lower()]

    # 2. Фильтр по количеству игроков
    players_filter = request.GET.get('players', '')
    if players_filter:
        try:
            players = int(players_filter)
            games = games.filter(min_players__lte=players, max_players__gte=players)
        except:
            pass

    # 3. Фильтр по времени (диапазон)
    time_min = request.GET.get('time_min', '')
    time_max = request.GET.get('time_max', '')

    if time_min:
        try:
            t_min = int(time_min)
            games = games.filter(
                Q(min_duration__isnull=True, max_duration__isnull=True) |
                Q(min_duration__lte=t_min, max_duration__gte=t_min) |
                Q(min_duration__lte=t_min, max_duration__isnull=True) |
                Q(min_duration__isnull=True, max_duration__gte=t_min)
            )
        except:
            pass

    if time_max:
        try:
            t_max = int(time_max)
            games = games.filter(
                Q(min_duration__isnull=True, max_duration__isnull=True) |
                Q(min_duration__lte=t_max) |
                Q(max_duration__lte=t_max)
            )
        except:
            pass

    # 4. Фильтр по возрасту (ОТ скольки лет)
    age_min = request.GET.get('age_min', '')
    age_max = request.GET.get('age_max', '')

    # Если заполнены оба поля — используем тот, который заполнен
    if age_min and age_max:
        # Если оба заполнены — предупреждение, используем только age_min
        age_max = ''

    if age_min:
        try:
            a_min = int(age_min)
            games = games.filter(
                Q(min_age__isnull=True, max_age__isnull=True) |
                Q(min_age__gte=a_min) |
                Q(min_age__isnull=True, max_age__gte=a_min)
            )
            games = games.exclude(
                Q(max_age__lt=a_min) & ~Q(max_age__isnull=True)
            )
        except:
            pass

    # 5. Фильтр по возрасту (ДО скольки лет)
    if age_max:
        try:
            a_max = int(age_max)
            games = games.filter(
                Q(min_age__isnull=True, max_age__isnull=True) |
                Q(max_age__lte=a_max) |
                Q(min_age__lte=a_max)
            )
        except:
            pass

    return render(request, 'games/game_list.html', {'games': games})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Game
from users.models import OwnedGame

@login_required
def add_to_collection(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    OwnedGame.objects.get_or_create(user=request.user, game=game)
    return redirect('games')

@login_required
def remove_from_collection(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    OwnedGame.objects.filter(user=request.user, game=game).delete()
    return redirect('games')