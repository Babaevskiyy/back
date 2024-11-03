FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=backend.settings
ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "./wait-for-it.sh db:5432 -- python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]

