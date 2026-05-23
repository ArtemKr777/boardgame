FROM python:3.12-slim

WORKDIR /app

# Копируем requirements.txt из папки blog
COPY blog/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект из папки blog
COPY blog/ .

# Применяем миграции и собираем статику
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

CMD ["python", "manage.py", "runserver", "0.0.0.0:7860"]