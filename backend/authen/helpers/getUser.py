from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import HttpResponseForbidden
from backend.users.models import User

def getUserFromRequest(self_or_request):
    """
    Authenticate the user from the request or self_or_request object.

    Args:
        self_or_request (Request or View): The request object or the view itself.

    Returns:
        tuple: (user, error_message), where user is the authenticated user or None, 
               and error_message is a string with an error message or None.
    """
    # Determine if this is a class-based view
    is_class_based = hasattr(self_or_request, "request")

    if is_class_based:
        request = self_or_request.request
    else:
        request = self_or_request

    jwtAuth = JWTAuthentication()
    try:
        auth_result = jwtAuth.authenticate(request)
    except Exception as e:
        return None, f"Access denied: {e}"

    if auth_result is None:
        return None, "Access denied: Invalid or missing token."

    user, _ = auth_result
    return user, None
