from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import JWTToken


class IsNotBlacklisted(permissions.BasePermission):
    """
    Custom permission to check if the JWT token is blacklisted.

    This permission class ensures that the JWT token provided in the request
    is not blacklisted before allowing access to the view. If the token is
    blacklisted, access is denied.

    The comments below describe roughly the authentication flow
    """

    def has_permission(self, request, view):

        # Step 1: Authenticate the request using JWTAuthentication
        jwt_auth = JWTAuthentication()
        auth_result = jwt_auth.authenticate(request)

        # Step 2: If authentication fails or no valid token is found, log the failure
        if auth_result is None:
            print("JWT authentication failed: No valid token found.")
            return False

        # Step 3: If authentication is successful, retrieve the user and token
        user, token = auth_result

        # Step 4: Query the JWTToken model to check if the token is blacklisted
        jwt_token = JWTToken.objects.filter(user=user, token=token).last()

        if jwt_token:
            # Step 5: If the token is blacklisted, deny access and log the event
            if jwt_token.is_blacklisted:
                print(f"Access denied for user {user.username}: Token is blacklisted.")
                return False

            # Step 6: If the token is not blacklisted, grant access and log the event
            print(f"Access granted for user {user.username}: Token is not blacklisted.")
        else:
            print(f"No JWTToken found for user {user.username}.")
            return False

        return True

class IsSuperUser(permissions.BasePermission):
    """
    Allows access only to superusers.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)