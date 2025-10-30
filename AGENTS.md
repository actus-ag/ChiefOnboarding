# ChiefOnboarding - Agent Instructions

## Project Overview

ChiefOnboarding is a Django-based employee onboarding platform with Slack integration. The main backend code is in the `back/` directory.

### How ChiefOnboarding Works

ChiefOnboarding helps companies automate and streamline their employee onboarding process through:

#### Core Concepts

**Sequences**: Timeline-based onboarding paths that map out a new hire's journey. Sequences consist of blocks:
- **General blocks**: Trigger before/after start date or based on task completion
- **Unconditioned block**: Items automatically added when sequence is assigned (e.g., preboarding pages)
- All blocks trigger at 8 AM in the new hire's timezone
- Supports multiple timezones and languages (EN, DE, FR, ES, PT, TR, JA)

**Templates**: Reusable content items that can be added to sequences:
- **To Do Items**: Tasks for new hires with due dates, content, and optional forms
- **Resources**: Information/documentation, can be converted to courses with chapters and quizzes
- **Introductions**: Introduce colleagues to new hires
- **Badges**: Motivational rewards for completing milestones
- **Admin Tasks**: Tasks assigned to colleagues/managers
- **Messages**: One-off emails/Slack/text messages to new hires, managers, or channels

#### User Roles

- **Administrators**: Full dashboard access, can create/manage everything
- **Managers**: Limited access to their new hires, templates, and their admin tasks
- **Employees**: Basic accounts, visible on colleagues page, can access assigned resources
- **New Hires**: Onboarding participants with access to their tasks, resources, and portal

#### Integration Points

- **Slack Bot**: Primary interface for new hires, sends daily reminders, handles forms/courses
- **Web Portal**: Standalone alternative to Slack, includes all features
- **API**: Programmatic new hire creation and management
- **Auto-creation**: Automatically create new hires when they join Slack (with optional approval)

## Memorizing Standards

To permanently memorize project-specific standards, conventions, or patterns:

1. Add them to this AGENTS.md file in the appropriate section
2. Commit the changes with a descriptive message
3. The AI agent will automatically read and follow these instructions on future sessions

For more information, see: https://ona.com/docs/ona/agents-md

## Git Workflow

**IMPORTANT**: Follow this workflow for all changes:

1. **Automatic Commit**: After completing each task, automatically commit changes with a descriptive message
   - Use format: `<type>: <description>` with Co-authored-by: Ona <no-reply@ona.com>
   - Common types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`
   - Example: `feat: add new hire notification system`
   
2. **Ask Before Push**: ALWAYS ask the user if they want to push after committing
   - Never push automatically
   - Wait for explicit confirmation before running `git push`

## Development Environment

### Auto-Login for Debugging

The project includes a development-only auto-login feature for efficient debugging:

- **Admin credentials**: `admin@example.com` / `admin`
- **Control**: Set `DEV_AUTO_LOGIN=True` in `.env` to enable automatic login
- **Production**: Set `DEV_AUTO_LOGIN=False` or omit it entirely for production deployments
- **Setup command**: `python manage.py setup_dev_environment` creates the organization and admin user

This feature automatically logs you in as the admin user when accessing the application in development mode, eliminating the need for manual login during debugging.

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
