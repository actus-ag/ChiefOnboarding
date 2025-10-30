import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import management
from django.db import transaction
from django.utils import timezone
from django.utils.crypto import get_random_string

from organization.models import Organization
from slack_bot.models import SlackChannel
from users.models import User


class Command(management.BaseCommand):
    help = "Setup development environment with demo organization and admin user"

    def handle(self, *args, **options):
        if Organization.objects.exists():
            self.stdout.write(
                self.style.SUCCESS("Organization already exists, skipping setup")
            )
            return

        with transaction.atomic():
            # Create default Slack channel if it doesn't exist
            general_channel, _ = SlackChannel.objects.get_or_create(
                name="general", defaults={"channel_id": "C000000000"}
            )

            # Create organization
            org = Organization.objects.create(
                name="Demo Organization",
                timezone="UTC",
                language="en",
                slack_default_channel=general_channel,
            )

            # Create admin user
            admin_user = get_user_model().objects.create(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                language=org.language,
                timezone=org.timezone,
                role=get_user_model().Role.ADMIN,
                is_staff=True,
                is_superuser=True,
            )
            admin_user.set_password("admin")
            admin_user.save()

            # Load fixtures
            welcome_message_path = os.path.join(
                settings.BASE_DIR, "fixtures/welcome_message.json"
            )
            all_path = os.path.join(settings.BASE_DIR, "fixtures/all.json")

            if os.path.exists(welcome_message_path):
                management.call_command("loaddata", welcome_message_path, verbosity=0)
            if os.path.exists(all_path):
                management.call_command("loaddata", all_path, verbosity=0)

            # Update demo user if it exists
            try:
                demo_user = User.objects.get(email="john@chiefonboarding.com")
                demo_user.set_unusable_password()
                demo_user.unique_url = get_random_string(length=8)
                demo_user.start_day = timezone.now().date() + timedelta(days=5)
                demo_user.save()
            except User.DoesNotExist:
                pass

            self.stdout.write(
                self.style.SUCCESS(
                    "Development environment setup complete!\n"
                    "Admin user: admin@example.com / admin"
                )
            )
