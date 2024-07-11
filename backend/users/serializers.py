"""
Serializer for User Model.

Includes:
- UserSerializer: Serializes/deserializes User objects.
"""

from django.conf import settings
from django.contrib.auth import authenticate
from .models import User
from backend.authen.models import JWTToken
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }


from django.utils import timezone

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user is None or not check_password(password, user.password):
            raise serializers.ValidationError('Invalid username or password')

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        # Make expires_at timezone-aware
        expires_at = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

        jwt_token = JWTToken.objects.create(
            user=user,
            token=access_token,
            expires_at=expires_at,
        )

        # Return JSON serializable data
        return {
            'username': user.username,
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': expires_at,
            }
        }


