"""
This module defines a decorator to enforce user permissions and authentication in Django views.

**permission_required** (decorator):
    A decorator to check if a user has the required permissions to access a view. It ensures that the user is authenticated and has at least one of the specified permissions.

    Args:
        permissions (list or str): 
            - A single permission string or a list of permission strings required for access.

    Returns:
        function: 
            The decorated view function. If the user does not meet the required permissions, they receive an `HttpResponseForbidden` response.

    Usage:
        @permission_required("readDevices")
        def some_view(request):
            # View logic here

        @permission_required(["editDevices", "createDevices"])
        def another_view(request):
            # View logic here

    Functionality:
        - The decorator first checks if the user is authenticated by calling `getUserFromRequest`.
        - If the user is authenticated but does not have the required permissions, an `HttpResponseForbidden` is returned with an error message.
        - The decorator can be applied to any Django view function to enforce permission checks.
"""


from functools import wraps
from django.http import HttpResponseForbidden

from backend.authen.helpers.getUser import getUserFromRequest

def permission_required(permissions):
    """
    Decorator to check user permissions and authentication.

    Args:
        permissions (list or str): Required permissions for access.

    Returns:
        function: The decorated view function.
    """
    if isinstance(permissions, str):
        permissions = [permissions]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self_or_request, *args, **kwargs):
            # Authenticate user
            user, error_message = getUserFromRequest(self_or_request)

            if user is None:
                return HttpResponseForbidden(error_message)

            # # Superuser check
            # if user.is_superuser:
            #     # Superusers can access everything
            #     return view_func(self_or_request, *args, **kwargs)

            # Permission check for non-superusers
            if not any(perm in user.permissions for perm in permissions):
                return HttpResponseForbidden("Access denied: Insufficient permissions.")

            return view_func(self_or_request, *args, **kwargs)

        return _wrapped_view

    return decorator
