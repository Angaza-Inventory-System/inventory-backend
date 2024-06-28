"""
API views and serializers for managing devices, warehouses, and donors.

Views:
- DeviceListCreate: API endpoint to list all devices or create a new device.
- DeviceRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a device.
- WarehouseListCreate: API endpoint to list all warehouses or create a new warehouse.
- WarehouseRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a warehouse.
- DonorListCreate: API endpoint to list all donors or create a new donor.
- DonorRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a donor.

Serializers:
- DeviceSerializer: Serializes Device model data for API interactions.
- WarehouseSerializer: Serializes Warehouse model data for API interactions.
- DonorSerializer: Serializes Donor model data for API interactions.
"""

from rest_framework import generics

from .models import Device, Donor, Warehouse
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer


class DeviceListCreate(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class DeviceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class WarehouseListCreate(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class DonorListCreate(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


class DonorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
