from django.http import HttpResponseForbidden
from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User

def get_user_from_token(token):
    if not token:
        return None
    try:
        decoded_token = JWTAuthentication().get_validated_token(token)
        user_id = decoded_token.get('user_id')
        return User.objects.get(id=user_id)
    except (JWTAuthentication.InvalidToken, User.DoesNotExist, KeyError):
        return None

def permission_required(permission):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            jwt_auth = JWTAuthentication()
            try:
                auth_result = jwt_auth.authenticate(request)
            except Exception as e:
                return HttpResponseForbidden(f"Access denied: {e}")

            if auth_result is None:
                return HttpResponseForbidden("Access denied: Invalid or missing token.")

            user, _ = auth_result

            if not user.permissions.get(permission, False):
                return HttpResponseForbidden("Access denied: Insufficient permissions.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator
