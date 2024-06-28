"""
API views and serializers for managing devices, warehouses, and donors.

Views:
- DeviceListCreate: API endpoint to list all devices or create a new device.
- DeviceRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a device.
- WarehouseListCreate: API endpoint to list all warehouses or create a new warehouse.
- WarehouseRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a warehouse.
- DonorListCreate: API endpoint to list all donors or create a new donor.
- DonorRetrieveUpdateDestroy: API endpoint to retrieve, update, or delete a donor.

ViewSets:
- DeviceViewSet: Provides CRUD operations for devices.
- WarehouseViewSet: Provides CRUD operations for warehouses.
- DonorViewSet: Provides CRUD operations for donors.

Serializers:
- DeviceSerializer: Serializes Device model data for API interactions.
- WarehouseSerializer: Serializes Warehouse model data for API interactions.
- DonorSerializer: Serializes Donor model data for API interactions.
"""

from rest_framework import generics, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Device, Donor, Warehouse
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer
from .pagination import CustomPagination

class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'type': ['exact', 'icontains'],
        'make': ['exact', 'icontains'],
        'model': ['exact', 'icontains'],
        'year_of_manufacture': ['exact', 'gte', 'lte'],
        'status': ['exact'],
        'operating_system': ['exact', 'icontains'],
        'physical_condition': ['exact', 'icontains'],
        'donor__name': ['exact', 'icontains'],
        'location__name': ['exact', 'icontains'],
        'assigned_user__username': ['exact', 'icontains'],
    }
    ordering_fields = ['type', 'make', 'model', 'year_of_manufacture', 'status']
    ordering = ['type']


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'warehouse_number': ['exact'],
        'name': ['icontains'],
        'country': ['exact', 'icontains'],
        'city': ['exact', 'icontains'],
        'postal_code': ['exact'],
        'phone': ['exact'],
    }
    ordering_fields = ['warehouse_number', 'name', 'country', 'city', 'postal_code', 'phone']
    ordering = ['warehouse_number']


class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        'name': ['icontains'],
        'contact_info': ['icontains'],
        'address': ['icontains'],
        'email': ['exact', 'icontains'],
        'phone': ['exact'],
    }
    ordering_fields = ['name', 'email', 'phone']
    ordering = ['name']


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
