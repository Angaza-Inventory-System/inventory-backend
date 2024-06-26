"""
Serializer for User Model.

Includes:
- UserSerializer: Serializes/deserializes User objects.
"""

from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
