"""
Serializers for JWTToken model.

Serializers:
- AuthSerializer: Serializes JWTToken model data for API interactions.
"""

from rest_framework import serializers

from .models import JWTToken


class AuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = JWTToken
        fields = "__all__"
