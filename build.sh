#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies efficiently
python -m pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Collect static files and migrate
python manage.py collectstatic --noinput
python manage.py migrate