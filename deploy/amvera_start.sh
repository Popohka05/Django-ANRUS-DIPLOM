#!/usr/bin/env bash
set -o errexit

export AMVERA=${AMVERA:-true}
export DEBUG=${DEBUG:-False}
export DATA_DIR=${DATA_DIR:-/data}

python manage.py collectstatic --no-input
python manage.py migrate --no-input
python manage.py load_demo_words

exec gunicorn english_vocab_trainer.wsgi:application --bind "0.0.0.0:${PORT:-80}"
