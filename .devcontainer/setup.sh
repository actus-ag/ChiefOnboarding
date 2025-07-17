#!/bin/bash
set -e

echo "Setting up development environment..."

# Generate a unique secret key for this instance
SECRET_KEY=$(python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
export SECRET_KEY

echo "Generated new Django secret key"

# Run database migrations
echo "Running database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete!"
