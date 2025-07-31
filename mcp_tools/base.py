"""Base classes and infrastructure for ChiefOnboarding MCP tools."""

import logging
from functools import wraps
from typing import Any, Dict, List, Optional

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError, PermissionDenied
from django.db import transaction, IntegrityError
from django.db.models import Model
from mcp_server import MCPToolset, ModelQueryToolset

User = get_user_model()
logger = logging.getLogger(__name__)


class ChiefOnboardingPermissionError(Exception):
    """Custom exception for permission-related errors."""
    pass


class ChiefOnboardingValidationError(Exception):
    """Custom exception for validation-related errors."""
    pass


def require_permission(permission_check):
    """
    Decorator to check permissions before executing MCP tool methods.
    
    Args:
        permission_check: Function that takes (user, *args, **kwargs) and returns bool
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            user = getattr(self, 'user', None)
            if not user or not user.is_authenticated:
                raise ChiefOnboardingPermissionError("Authentication required")
            
            if not permission_check(user, *args, **kwargs):
                raise ChiefOnboardingPermissionError(
                    f"Permission denied for {func.__name__}"
                )
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def validate_input(**validators):
    """
    Decorator to validate input parameters.
    
    Args:
        **validators: Dict of parameter_name: validation_function pairs
    """
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Get function parameter names
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(self, *args, **kwargs)
            bound_args.apply_defaults()
            
            # Validate each parameter
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ChiefOnboardingValidationError(
                            f"Invalid value for parameter '{param_name}': {value}"
                        )
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


def handle_exceptions(func):
    """Decorator to handle common exceptions and provide consistent error messages."""
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except ChiefOnboardingPermissionError as e:
            logger.error(f"Permission error in {func.__name__}: {e}")
            return {"error": str(e), "type": "permission_error"}
        except ChiefOnboardingValidationError as e:
            logger.error(f"Validation error in {func.__name__}: {e}")
            return {"error": str(e), "type": "validation_error"}
        except ValidationError as e:
            logger.error(f"Django validation error in {func.__name__}: {e}")
            return {"error": str(e), "type": "validation_error"}
        except PermissionDenied as e:
            logger.error(f"Django permission denied in {func.__name__}: {e}")
            return {"error": str(e), "type": "permission_error"}
        except IntegrityError as e:
            logger.error(f"Database integrity error in {func.__name__}: {e}")
            return {"error": "Database integrity error", "type": "database_error"}
        except Exception as e:
            logger.exception(f"Unexpected error in {func.__name__}: {e}")
            return {"error": "An unexpected error occurred", "type": "internal_error"}
    return wrapper


class BaseChiefOnboardingToolset(MCPToolset):
    """Base toolset class for ChiefOnboarding MCP tools."""
    
    def __init__(self, user=None):
        super().__init__()
        self.user = user
    
    def is_admin(self, user=None) -> bool:
        """Check if user is an admin."""
        user = user or self.user
        return user and hasattr(user, 'role') and user.role == User.Role.ADMIN
    
    def is_manager(self, user=None) -> bool:
        """Check if user is a manager or admin."""
        user = user or self.user
        return user and hasattr(user, 'role') and user.role in [User.Role.ADMIN, User.Role.MANAGER]
    
    def is_new_hire(self, user=None) -> bool:
        """Check if user is a new hire."""
        user = user or self.user
        return user and hasattr(user, 'role') and user.role == User.Role.NEWHIRE
    
    def can_manage_users(self, user=None) -> bool:
        """Check if user can manage other users."""
        return self.is_manager(user)
    
    def can_access_admin_features(self, user=None) -> bool:
        """Check if user can access admin features."""
        return self.is_admin(user)
    
    def can_manage_organization(self, user=None) -> bool:
        """Check if user can manage organization settings."""
        return self.is_admin(user)


class BaseModelQueryToolset(ModelQueryToolset):
    """Base model query toolset with permission checking."""
    
    def __init__(self, user=None):
        super().__init__()
        self.user = user
    
    def get_queryset(self):
        """Override to add permission-based filtering."""
        queryset = super().get_queryset()
        
        # Apply user-based filtering
        if self.user and hasattr(self, 'filter_by_user'):
            queryset = self.filter_by_user(queryset)
        
        return queryset
    
    def filter_by_user(self, queryset):
        """Override in subclasses to implement user-specific filtering."""
        return queryset


# Common validation functions
def validate_email(email: str) -> bool:
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_non_empty_string(value: str) -> bool:
    """Validate that string is not empty."""
    return isinstance(value, str) and value.strip() != ""


def validate_positive_integer(value: int) -> bool:
    """Validate that value is a positive integer."""
    return isinstance(value, int) and value > 0


def validate_date_string(date_str: str) -> bool:
    """Validate date string format (YYYY-MM-DD)."""
    import re
    from datetime import datetime
    
    if not isinstance(date_str, str):
        return False
    
    # Check format
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_str):
        return False
    
    # Check if valid date
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Permission check functions
def admin_required(user, *args, **kwargs) -> bool:
    """Permission check for admin-only operations."""
    return user and hasattr(user, 'role') and user.role == User.Role.ADMIN


def manager_required(user, *args, **kwargs) -> bool:
    """Permission check for manager/admin operations."""
    return user and hasattr(user, 'role') and user.role in [User.Role.ADMIN, User.Role.MANAGER]


def authenticated_required(user, *args, **kwargs) -> bool:
    """Permission check for authenticated users."""
    return user and user.is_authenticated