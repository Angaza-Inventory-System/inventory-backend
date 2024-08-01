"""
Serializers for User model instances and user login authentication.

Serializers:
- UserSerializer: Serializes User model instances.
- UserLoginSerializer: Validates user login credentials and generates JWT tokens.

UserSerializer Fields:
- username (str): The username of the user.
- password (str, write-only): The password of the user (not retrieved in responses).
- email (str): The email address of the user.
- role (str): The role of the user.
- first_name (str): The first name of the user.
- last_name (str): The last name of the user.

UserLoginSerializer Fields:
- username (str): The username provided for login.
- password (str, write-only): The password provided for login.

UserLoginSerializer Validation:
- Validates the provided username and password against existing User records.
- Generates new JWT tokens for authenticated users.
- Blacklists existing tokens for the authenticated user.
"""

from django.conf import settings
from django.utils import timezone
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from backend.authen.models import JWTToken

from .models import User


class UserSerializer(serializers.ModelSerializer):
    permissions = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "email",
            "role",
            "first_name",
            "last_name",
            "is_superuser",
            "permissions",
        ]
        extra_kwargs = {
            "permissions": {"read_only": True},
            "password": {"write_only": True},
        }


class UserPermissionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["permissions"]

class UserPasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["password"]

    def validate_password(self, value):
        password_validator = RegexValidator(
            regex="^(?=.*\\d)(?=.*[!@#$%^&*])(?=.*[A-Z]).{10,128}$",
            message="Password must be at least 10 characters long and include at least one digit, one special character, and one uppercase letter."
        )
        try:
            password_validator(self.password)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return value


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError(f"Invalid username or password {user} {user.check_password(password)}")

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        expires_at = timezone.now() + settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]

        JWTToken.objects.create(
            user=user,
            token=access_token,
            expires_at=expires_at,
        )

        return {
            "username": user.username,
            "user_id": user.id,
            "tokens": {
                "access_token": access_token,
                "expires_at": expires_at,
            },
        }

    def update(self, instance, validated_data):
        # Required, but not used for login
        pass

    def create(self, validated_data):
        # Required, but not used for login
        pass
