release: uv run python back/manage.py createcachetable && uv run python back/manage.py migrate
web: uv run gunicorn --chdir back back.wsgi
worker: uv run python back/manage.py qcluster
