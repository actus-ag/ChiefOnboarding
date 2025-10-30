from django.conf import settings
from django.contrib.auth import get_user_model, login
from django.http import HttpResponse
from django.shortcuts import redirect

from organization.models import Organization


# Credits: https://stackoverflow.com/a/64623669
class HealthCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == "/health":
            return HttpResponse("ok")
        return self.get_response(request)


class SetupOrgMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        org = Organization.object.get()
        if org is None and request.path != "/setup/":
            return redirect("setup")
        return self.get_response(request)


class DevAutoLoginMiddleware:
    """
    Middleware for development that automatically logs in as admin user.
    Only active when DEBUG=True and DEV_AUTO_LOGIN=True.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Only run in development mode with explicit flag
        if (
            settings.DEBUG
            and getattr(settings, "DEV_AUTO_LOGIN", False)
            and not request.user.is_authenticated
        ):
            # Skip auto-login for specific paths
            skip_paths = ["/api/", "/static/", "/media/"]
            if not any(request.path.startswith(path) for path in skip_paths):
                # Try to get admin user
                User = get_user_model()
                try:
                    admin_user = User.objects.filter(
                        role=User.Role.ADMIN, email="admin@example.com"
                    ).first()
                    if admin_user:
                        login(
                            request,
                            admin_user,
                            backend="django.contrib.auth.backends.ModelBackend",
                        )
                except Exception:
                    pass

        response = self.get_response(request)
        return response
