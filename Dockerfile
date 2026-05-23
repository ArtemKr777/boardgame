# Используем официальный образ Python
FROM python:3.12-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Применяем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# Запускаем сервер разработки Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]