# ChiefOnboarding - Agent Instructions

## Project Overview

ChiefOnboarding is a Django-based employee onboarding platform with Slack integration. The main backend code is in the `back/` directory.

## Git Workflow

**IMPORTANT**: Follow this workflow for all changes:

1. **Automatic Commit**: After completing each task, automatically commit changes with a descriptive message
   - Use format: `<type>: <description>` with Co-authored-by: Ona <no-reply@ona.com>
   - Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   - Example: `feat: add new hire notification system`
   
2. **Ask Before Push**: ALWAYS ask the user if they want to push after committing
   - Never push automatically
   - Wait for explicit confirmation before running `git push`

## Development Commands

### Testing

```bash
cd back
pytest --cov=. --cov-report=xml
```

### Linting & Formatting

```bash
cd back
ruff check .
ruff format . --check
```

### Database Operations

```bash
cd back
python manage.py migrate
python manage.py makemigrations --check
```

### Fixtures & Setup

```bash
cd back
python manage.py shell < fixtures/init_testing.py
python manage.py loaddata all.json
python manage.py loaddata welcome_message.json
```

### Internationalization

```bash
cd back
# Extract new translatable strings and update .po files
python manage.py makemessages -l de

# Compile .po files to .mo files (required after any translation changes)
python manage.py compilemessages
```

**Important**: `.mo` files are not automatically updated and must be compiled manually after any changes to `.po` files. They are not version controlled (in .gitignore).

## Code Style

- Python 3.11
- Django framework
- Line length: 88 characters (flake8 config)
- Uses ruff for linting and formatting
- Import sorting enabled in ruff config

## Project Structure

- `back/` - Main Django application
- `back/manage.py` - Django management script
- `back/back/` - Django settings and configuration
- `back/*/` - Django apps (admin, api, new_hire, etc.)
- Tests use pytest with coverage reporting

## Dependencies

- Django <5
- PostgreSQL database
- Slack Bolt for Slack integration
- Django Q2 for background tasks
- Various other packages in Pipfile
