from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from games.models import Game

@login_required
def recommendations_view(request):
    """
    Отображает страницу с рекомендациями.
    Временно показывает популярные игры, пока ML-модуль не готов.
    """
    # Показываем популярные игры по среднему рейтингу
    # (временно, пока ML не готов)
    popular_games = Game.objects.all().order_by('-id')[:10]
    
    recommendations = []
    for idx, game in enumerate(popular_games, start=1):
        recommendations.append({
            'rank': idx,
            'game_id': game.id,
            'game_name': game.name,
            'avg_rating': 4.5,  # Заглушка
            'final_score': round(5.0 - idx * 0.3, 2)
        })
    
    context = {
        'recommendations': recommendations,
        'has_recommendations': len(recommendations) > 0
    }
    return render(request, 'recommendations/recommendations.html', context)