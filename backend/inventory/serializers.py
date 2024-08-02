"""
Serializers for the inventory management system.

This module defines serializers for the models used in the inventory system,
providing functionality for serializing and deserializing data for various API
endpoints.

BaseSerializer:
- A base serializer class that provides common functionality for handling related
  fields and customizing the representation of serialized data. It includes:
  - `create_related_fields(fields)`: Dynamically creates fields for related models
    and adds their serializers.
  - `to_representation(instance)`: Customizes the output representation of
    serialized data by including detailed representations of related fields.

LocationSerializer:
- Serializer for the Location model.
- Inherits from BaseSerializer and includes all fields from the Location model.
- Does not include any related fields.

DonorSerializer:
- Serializer for the Donor model.
- Inherits from BaseSerializer and includes all fields from the Donor model.
- Does not include any related fields.

ShipmentSerializer:
- Serializer for the Shipment model.
- Inherits from BaseSerializer and includes all fields from the Shipment model.
- Includes a related field for `destination`, which is a foreign key to the Location model.
- `destination` field is represented using the LocationSerializer.

DeviceSerializer:
- Serializer for the Device model.
- Inherits from BaseSerializer and includes all fields from the Device model.
- Sets `device_id` as read-only.
- Includes related fields for:
  - `donor`: Represented using the DonorSerializer.
  - `start_location` and `end_location`: Represented using the LocationSerializer.
  - `created_by` and `received_by`: Represented using the UserSerializer.
  - `shipping_infos`: Represented using the ShipmentSerializer.

Each related field in the DeviceSerializer is dynamically created in the `__init__`
method, allowing for detailed nested representations in API responses.
"""

from rest_framework import serializers
from backend.users.serializers import UserSerializer
from backend.users.models import User

from .models import Device, Donor, Location, Shipment

class BaseSerializer(serializers.ModelSerializer):
    def create_related_fields(self, fields):
        for field_name, model_class, serializer_class in fields:
            self.fields[f'{field_name}'] = serializers.PrimaryKeyRelatedField(
                queryset=model_class.objects.all(), write_only=True
            )
            self.fields[f'{field_name}_detail'] = serializer_class(
                source=field_name, read_only=True
            )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for field_name in self.Meta.related_fields:
            representation[field_name] = representation.pop(f'{field_name}_detail')
        return representation


class LocationSerializer(BaseSerializer):
    class Meta:
        model = Location
        fields = "__all__"
        related_fields = []


class DonorSerializer(BaseSerializer):
    class Meta:
        model = Donor
        fields = "__all__"
        related_fields = []


class ShipmentSerializer(BaseSerializer):
    class Meta:
        model = Shipment
        fields = "__all__"
        related_fields = ['destination']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_related_fields([
            ('destination', Location, LocationSerializer)
        ])


class DeviceSerializer(BaseSerializer):
    class Meta:
        model = Device
        fields = "__all__"
        read_only_fields = ["device_id"]
        related_fields = [
            'donor', 
            'start_location', 
            'end_location', 
            'created_by', 
            'received_by', 
            'shipping_infos'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_related_fields([
            ('donor', Donor, DonorSerializer),
            ('start_location', Location, LocationSerializer),
            ('end_location', Location, LocationSerializer),
            ('created_by', User, UserSerializer),
            ('received_by', User, UserSerializer),
            ('shipping_infos', Shipment, ShipmentSerializer)
        ])
