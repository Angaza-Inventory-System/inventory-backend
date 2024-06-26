"""
Serializers for Device, Warehouse and Donor models.

Serializers:
- DeviceSerializer: Serializes Device model instances.
- WarehouseSerializer: Serializes Warehouse model instances.
- DonorSerializer: Serializes Donor model instances.
"""

from rest_framework import serializers
from .models import Device, Warehouse, Donor

class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = '__all__'