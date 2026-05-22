import os
import sys
import subprocess

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

# Запускаем сервер
subprocess.run([sys.executable, 'manage.py', 'migrate'])
subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'])
subprocess.run([sys.executable, 'manage.py', 'runserver', '0.0.0.0:7860'])