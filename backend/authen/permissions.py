from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import JWTToken

class IsNotBlacklisted(permissions.BasePermission):
    """
    Custom permission to check if the JWT token is blacklisted.
    """

    def has_permission(self, request, view):
        jwt_auth = JWTAuthentication()
        auth_result = jwt_auth.authenticate(request)

        if auth_result is None:
            print("JWT authentication failed: No valid token found.")

        user, token = auth_result

        if user is None:
            return False
        jwt_token = JWTToken.objects.filter(user=user, token=token).last()
        if jwt_token:
            if jwt_token.is_blacklisted:
                print(f"Access denied for user {user.username}: Token is blacklisted.")
                return False  # Token is blacklisted, deny access
            else:
                print(f"Access granted for user {user.username}: Token is not blacklisted.")
        else:
            print(f"No JWTToken found for user {user.username}.")
            return False

        return True  # Permission granted if no issues found
