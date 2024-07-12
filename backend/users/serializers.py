from django.conf import settings
from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from backend.authen.models import JWTToken

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        user = User.objects.filter(username=username).first()
        if user is None or not user.check_password(password):
            raise serializers.ValidationError('Invalid username or password')

        # Blacklist existing tokens for the user in your custom model
        JWTToken.objects.filter(user=user).update(is_blacklisted=True)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        expires_at = timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']

        # Save the new token in your custom model
        jwt_token = JWTToken.objects.create(
            user=user,
            token=access_token,
            expires_at=expires_at,
        )

        return {
            'username': user.username,
            'tokens': {
                'access_token': access_token,
                'refresh_token': refresh_token,
                'expires_at': expires_at,
            }
        }
