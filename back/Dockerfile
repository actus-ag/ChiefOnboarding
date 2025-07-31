FROM python:3.11
RUN apt-get update
RUN mkdir /var/run/supervisord
RUN mkdir /var/log/supervisord
RUN apt-get install -y supervisor gettext

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONUNBUFFERED 1
RUN mkdir -p /app
WORKDIR /app

# Copy project files and install dependencies
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --compile-bytecode

# Copy application code
COPY ./back/ ./back/
COPY ./back/supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Compile translations
RUN uv run django-admin compilemessages 

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
