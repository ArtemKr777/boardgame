import csv
import os
import re
from django.core.management.base import BaseCommand
from games.models import Game


class Command(BaseCommand):
    help = 'Load games from CSV file'

    def parse_duration(self, time_str):
        """Парсит время из форматов: 30, 30-45, 30+, 30-45+"""
        time_str = str(time_str).strip()
        time_str = time_str.replace('^', '').replace('`', '')
        if not time_str:
            return None, None

        time_str = time_str.replace('мин', '').strip()

        if '-' in time_str and '+' not in time_str:
            parts = time_str.split('-')
            min_d = int(parts[0].strip())
            max_d = int(parts[1].strip())
            return min_d, max_d

        if '+' in time_str:
            min_d = int(time_str.replace('+', '').strip())
            return min_d, None

        if time_str.isdigit():
            d = int(time_str)
            return d, d

        return None, None

    def parse_age(self, age_str):
        """Парсит возраст из форматов: 8+, 12+, 16-18"""
        age_str = str(age_str).strip()
        age_str = age_str.replace('^', '').replace('`', '')
        if not age_str:
            return None, None

        if '-' in age_str:
            parts = age_str.split('-')
            min_a = int(parts[0].strip())
            max_a = int(parts[1].strip())
            return min_a, max_a

        match = re.match(r'(\d+)', age_str)
        if match:
            age = int(match.group(1))
            return age, None

        return None, None

    def clean_list(self, value):
        """Очищает строку от кавычек, скобок и символа ^"""
        value = str(value).strip()
        value = value.strip('[]')
        value = value.replace("'", "")
        value = value.replace('"', '')
        value = value.replace('^', '')
        value = value.replace('`', '')
        value = value.replace('\n', '')
        value = value.replace('\r', '')
        items = [item.strip() for item in value.split(',') if item.strip()]
        return ', '.join(items)

    def handle(self, *args, **options):
        csv_file_path = 'games_data.csv'

        if not os.path.exists(csv_file_path):
            self.stdout.write(self.style.ERROR(f'Файл {csv_file_path} не найден!'))
            return

        self.stdout.write(f'Загрузка из файла: {csv_file_path}')

        # Очищаем старые данные
        Game.objects.all().delete()

        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file, delimiter=',')
            count = 0
            errors = 0

            for row in reader:
                try:
                    name = row.get('Name', '').strip()
                    name = name.replace('^', '').replace('`', '')
                    if not name:
                        continue

                    players_str = row.get('Count_Gamers', '').strip()
                    players_str = players_str.replace('^', '').replace('`', '')
                    if '-' in players_str:
                        min_players = int(players_str.split('-')[0])
                        max_players = int(players_str.split('-')[1])
                    elif players_str.isdigit():
                        min_players = int(players_str)
                        max_players = int(players_str)
                    else:
                        min_players = 1
                        max_players = 4

                    time_str = row.get('Time', '').strip()
                    min_duration, max_duration = self.parse_duration(time_str)

                    age_str = row.get('Age', '').strip()
                    min_age, max_age = self.parse_age(age_str)

                    thematics = self.clean_list(row.get('Thematics', ''))
                    categories = self.clean_list(row.get('Categories', ''))

                    Game.objects.create(
                        name=name,
                        min_players=min_players,
                        max_players=max_players,
                        min_duration=min_duration,
                        max_duration=max_duration,
                        min_age=min_age,
                        max_age=max_age,
                        thematics=thematics,
                        categories=categories,
                    )
                    count += 1

                except Exception as e:
                    errors += 1
                    self.stdout.write(self.style.WARNING(f'Ошибка в строке: {e}'))

            self.stdout.write(self.style.SUCCESS(f'\n✅ Загружено {count} игр! Ошибок: {errors}'))