from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from games.models import Game
from .models import GameRequest, RequestResponse

@login_required
def recommendations(request):
    similar_games = Game.objects.all()[:5]  # временно
    new_games = Game.objects.order_by('-id')[:5]
    game_requests = GameRequest.objects.filter(status='open').exclude(creator=request.user)
    my_requests = GameRequest.objects.filter(creator=request.user)
    return render(request, 'recommendations/recommendations.html', {
        'similar_games': similar_games,
        'new_games': new_games,
        'game_requests': game_requests,
        'my_requests': my_requests,
    })

@login_required
def create_request(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        game = Game.objects.get(id=game_id) if game_id else None
        GameRequest.objects.create(
            creator=request.user,
            game=game,
            description=request.POST.get('description', ''),
            desired_date=request.POST.get('desired_date') or None,
            location=request.POST.get('location', ''),
            max_players=request.POST.get('max_players', 4),
        )
        return redirect('recommendations')
    games = Game.objects.all()
    return render(request, 'recommendations/create_request.html', {'games': games})

@login_required
def respond_to_request(request, request_id):
    game_request = GameRequest.objects.get(id=request_id)
    if request.method == 'POST':
        RequestResponse.objects.create(
            request=game_request,
            user=request.user,
            message=request.POST.get('message', ''),
        )
        return redirect('recommendations')
    return render(request, 'recommendations/respond_request.html', {'game_request': game_request})