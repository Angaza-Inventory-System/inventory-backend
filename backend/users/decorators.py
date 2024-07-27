from django.http import HttpResponseForbidden
from functools import wraps

def permission_required(permission):
    """
    Decorator to check if the user has a specific permission.
    
    Args:
        permission (str): The permission to check (e.g., 'readDevices').
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user.permissions.get(permission, False):
                return HttpResponseForbidden("You do not have permission to access this resource.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
