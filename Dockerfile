FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV AMVERA=true
ENV DEBUG=False
ENV DATA_DIR=/data

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /data

EXPOSE 80

CMD sh -c "python manage.py collectstatic --no-input && python manage.py migrate --no-input && python manage.py load_demo_words && gunicorn english_vocab_trainer.wsgi:application --bind 0.0.0.0:${PORT:-80}"
