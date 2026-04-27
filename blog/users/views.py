from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from .models import Profile, OwnedGame, PlayedGame, PlayerResult
from games.models import Game

@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    owned_games = OwnedGame.objects.filter(user=request.user)
    played_games = PlayedGame.objects.filter(user=request.user).order_by('-play_date')
    return render(request, 'users/profile.html', {
        'profile': profile,
        'owned_games': owned_games,
        'played_games': played_games,
    })

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile.city = request.POST.get('city', '')
        profile.age = request.POST.get('age', '')
        profile.phone = request.POST.get('phone', '')
        profile.save()
        return redirect('profile')
    return render(request, 'users/edit_profile.html', {'profile': profile})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            return render(request, 'users/register.html', {'error': 'Пароли не совпадают'})

        if User.objects.filter(username=username).exists():
            return render(request, 'users/register.html', {'error': 'Пользователь с таким именем уже существует'})

        if User.objects.filter(email=email).exists():
            return render(request, 'users/register.html', {'error': 'Пользователь с таким email уже существует'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        Profile.objects.create(user=user)
        login(request, user)
        return redirect('games')

    return render(request, 'users/register.html')


@login_required
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    owned_games = OwnedGame.objects.filter(user=request.user)

    # Группировка сыгранных партий по играм
    played_games_by_game = {}
    for result in PlayerResult.objects.filter(player=request.user).select_related('played_game__game'):
        game = result.played_game.game
        if game not in played_games_by_game:
            played_games_by_game[game] = []
        played_games_by_game[game].append(result.played_game)

    return render(request, 'users/profile.html', {
        'profile': profile,
        'owned_games': owned_games,
        'played_games_by_game': played_games_by_game,
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        request.user.first_name = request.POST.get('first_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        profile.city = request.POST.get('city', '')
        profile.age = request.POST.get('age', '')
        profile.phone = request.POST.get('phone', '')
        profile.save()
        return redirect('profile')
    return render(request, 'users/edit_profile.html', {'profile': profile})


@login_required
def add_played_game(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.method == 'POST':
        # Создаём запись о партии
        played_game = PlayedGame.objects.create(
            user=request.user,
            game=game,
            duration_minutes=request.POST.get('duration') or None,
            comment=request.POST.get('comment', '')
        )

        # Обрабатываем участников
        # Формат: player_1_name, player_1_place, player_1_score
        i = 1
        while f'player_{i}_name' in request.POST:
            username = request.POST.get(f'player_{i}_name', '').strip()
            place = request.POST.get(f'player_{i}_place', '')
            score = request.POST.get(f'player_{i}_score', '')

            if username:
                try:
                    player = User.objects.get(username=username)
                    PlayerResult.objects.create(
                        played_game=played_game,
                        player=player,
                        place=int(place) if place else None,
                        score=int(score) if score else None
                    )
                except User.DoesNotExist:
                    pass  # Игрок не найден в системе
            i += 1

        return redirect('profile')

    # GET запрос — показываем форму
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'users/add_played_game.html', {'game': game, 'users': all_users})


@login_required
def user_list(request):
    query = request.GET.get('q', '')
    users = User.objects.exclude(id=request.user.id)

    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query)
        )

    return render(request, 'users/user_list.html', {'users': users, 'query': query})


@login_required
def user_profile_detail(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    profile = Profile.objects.get_or_create(user=other_user)[0]

    # Группировка сыгранных партий по играм
    played_games_by_game = {}
    for result in PlayerResult.objects.filter(player=other_user).select_related('played_game__game'):
        game = result.played_game.game
        if game not in played_games_by_game:
            played_games_by_game[game] = []
        played_games_by_game[game].append(result.played_game)

    return render(request, 'users/user_profile_detail.html', {
        'other_user': other_user,
        'profile': profile,
        'played_games_by_game': played_games_by_game,
    })