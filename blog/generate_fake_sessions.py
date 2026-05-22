import os
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from users.models import UserSessionLog
from django.contrib.auth.models import User

# Список пользователей
users = list(User.objects.all())
if not users:
    users = [None]

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Mozilla/5.0 (Linux; Android 13; SM-G998B) AppleWebKit/537.36 Chrome/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/118.0",
]

# Список дат с 5 по 16 мая 2026
dates = []
for day in range(5, 17):  # 5,6,7,8,9,10,11,12,13,14,15,16
    dates.append(datetime(2026, 5, day, 0, 0, 0))

NUM_SESSIONS = 50

print(f"Генерация {NUM_SESSIONS} тестовых сессий за период 5–16 мая 2026...")

created = 0
for i in range(NUM_SESSIONS):
    # Выбираем случайную дату из списка
    session_date = random.choice(dates)
    
    # Случайное время в течение дня (0-23 часа)
    random_hour = random.randint(0, 23)
    random_minute = random.randint(0, 59)
    random_second = random.randint(0, 59)
    
    session_start = session_date.replace(hour=random_hour, minute=random_minute, second=random_second)
    session_start = timezone.make_aware(session_start)
    
    # Длительность сессии от 5 до 90 минут
    duration_minutes = random.randint(5, 90)
    session_end = session_start + timedelta(minutes=duration_minutes)
    
    # Количество просмотров
    page_views = random.randint(1, 30)
    
    # Случайный пользователь
    user = random.choice(users)
    
    # Уникальный ключ сессии
    session_key = f"fake_{i}_{random.randint(10000, 99999)}_{int(session_start.timestamp())}"
    
    log = UserSessionLog(
        user=user,
        session_key=session_key,
        start_time=session_start,
        last_activity=session_end,
        page_views=page_views,
        user_agent=random.choice(user_agents),
        ip_address=random_ip(),
    )
    log.save()
    created += 1
    
    if (i + 1) % 5 == 0 or i == NUM_SESSIONS - 1:
        print(f"  📊 Создано {i+1} из {NUM_SESSIONS} сессий")

print(f"\n✅ Готово! Создано {created} тестовых сессий.")