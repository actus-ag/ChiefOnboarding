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
   - Copy `.env.example` to `.env` for development configuration
   - Generate a unique Django secret key for this instance
   - Build and start all services
   - Run database migrations
   - Collect static files
3. Once ready, the Django application will be available at `http://localhost:8000`

## Environment Configuration

The devcontainer automatically creates a `.env` file from `.env.example` during setup and generates a unique secret key. For production use or custom development settings:

1. Copy `.env.example` to `.env` manually if needed
2. The `SECRET_KEY` is automatically generated during devcontainer setup
3. Modify other settings as needed for your environment

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
