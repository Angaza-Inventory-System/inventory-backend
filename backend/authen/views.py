"""
API view for user authentication via login.

Views:
- login: API endpoint to authenticate a user and return user data with a JWT token.

Serializers:
- UserLoginSerializer: Serializes user login data for authentication.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from backend.users.serializers import UserLoginSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    
    serializer = UserLoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    response_data = serializer.validated_data
    return Response(response_data, status=status.HTTP_200_OK)

