from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response


def handle_exception(exception):
    """
    Handles exceptions and returns an appropriate response.

    :param exception: The exception instance to handle.
    :return: A Response object with the error message and status code.
    """
    if isinstance(exception, ValidationError):
        return Response(
            {"error": "Validation error", "details": str(exception)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    elif isinstance(exception, IntegrityError):
        return Response(
            {"error": "Integrity error", "details": str(exception)},
            status=status.HTTP_400_BAD_REQUEST,
        )
    else:
        # Handle other exceptions
        return Response(
            {"error": "An unexpected error occurred", "details": str(exception)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
