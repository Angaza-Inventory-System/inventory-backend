"""
Serializers for Device, Warehouse and Donor models.

Serializers:
- DeviceSerializer: Serializes Device model instances.
- WarehouseSerializer: Serializes Warehouse model instances.
- DonorSerializer: Serializes Donor model instances.
"""

from rest_framework import serializers

from .models import Device, Donor, Location


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["device_id"]


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = "__all__"
