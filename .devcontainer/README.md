# Development Container Setup

This devcontainer configuration provides a complete development environment for ChiefOnboarding with hot reloading enabled.

## Features

- **Hot Reloading**: The Django development server automatically reloads when you make changes to Python files
- **PostgreSQL Database**: Fully configured PostgreSQL instance
- **VS Code Extensions**: Pre-installed Python development extensions
- **Port Forwarding**: Automatic port forwarding for web server (8000) and database (5432)
- **Environment Variables**: Pre-configured for development

## Getting Started

1. Open this repository in GitHub Codespaces or VS Code with the Dev Containers extension
2. The container will automatically:
   - Build and start all services
   - Generate a unique Django secret key for this instance
   - Run database migrations
   - Collect static files
3. Once ready, the Django application will be available at `http://localhost:8000`

## Environment Configuration

The devcontainer automatically generates a unique Django secret key during setup. Environment variables are configured in `docker-compose.yml`:

- `DEBUG=True` - Development mode enabled
- `SECRET_KEY` - Automatically generated unique key 
- `DATABASE_URL` - PostgreSQL connection string
- `ALLOWED_HOSTS` - Includes localhost and Codespaces domains

For production deployment, you'll need to set these environment variables appropriately in your hosting environment.

## Services

- **Web Server**: Django development server on port 8000
- **Database**: PostgreSQL on port 5432
- **Background Tasks**: Django Q cluster for asynchronous tasks

## Development Commands

- `python manage.py runserver` - Start the development server
- `python manage.py migrate` - Run database migrations
- `python manage.py createsuperuser` - Create an admin user
- `python manage.py shell` - Open Django shell
- `python manage.py test` - Run tests

## Environment Variables

The `.env` file contains development-specific environment variables. Key variables:

- `DEBUG=True` - Enables Django debug mode
- `ALLOWED_HOSTS` - Includes codespaces domains for external access
- `DATABASE_URL` - PostgreSQL connection string

## Hot Reloading

The Django development server automatically reloads when you make changes to:
- Python files (.py)
- Template files (.html)
- Static files (CSS, JS)

No manual restart required during development!
