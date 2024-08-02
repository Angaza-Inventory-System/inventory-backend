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
