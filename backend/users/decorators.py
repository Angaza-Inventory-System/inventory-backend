from functools import wraps

from django.http import HttpResponseForbidden
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import User


def get_user_from_token(token):
    if not token:
        return None
    try:
        decoded_token = JWTAuthentication().get_validated_token(token)
        user_id = decoded_token.get("user_id")
        return User.objects.get(id=user_id)
    except (JWTAuthentication.InvalidToken, User.DoesNotExist, KeyError):
        return None


def permission_required(permissions):
    if isinstance(permissions, str):
        permissions = [permissions]

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self_or_request, *args, **kwargs):
            # Determine if this is a class-based view
            is_class_based = hasattr(self_or_request, "request")

            if is_class_based:
                request = self_or_request.request
            else:
                request = self_or_request

            jwt_auth = JWTAuthentication()
            try:
                auth_result = jwt_auth.authenticate(request)
            except Exception as e:
                return HttpResponseForbidden(f"Access denied: {e}")

            if auth_result is None:
                return HttpResponseForbidden("Access denied: Invalid or missing token.")

            user, _ = auth_result

            # Superuser check
            if user.is_superuser:
                # Superusers can access everything
                return view_func(self_or_request, *args, **kwargs)

            # For non-superusers, check specific permissions
            if not all(user.permissions.get(perm, False) for perm in permissions):
                return HttpResponseForbidden("Access denied: Insufficient permissions.")

            return view_func(self_or_request, *args, **kwargs)

        return _wrapped_view

    return decorator
