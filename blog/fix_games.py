import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from games.models import Game

games = Game.objects.all()
count = 0

for game in games:
    changed = False
    if '^' in game.name:
        game.name = game.name.replace('^', '')
        changed = True
    if '^' in game.thematics:
        game.thematics = game.thematics.replace('^', '')
        changed = True
    if '^' in game.categories:
        game.categories = game.categories.replace('^', '')
        changed = True

    if changed:
        game.save()
        count += 1
        print(f'Исправлено: {game.name}')

print(f'\n✅ Всего исправлено игр: {count}')