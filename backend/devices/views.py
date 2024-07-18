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

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, viewsets
from rest_framework.decorators import permission_classes
from haystack.query import SearchQuerySet
from backend.authen.permissions import IsNotBlacklisted
from .models import Device, Donor, Warehouse
from .pagination import CustomPagination
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer


class SearchAndLimitMixin:
    search_fields = []
    filterset_fields = []
    ordering_fields = []
    ordering = []

    def search_queryset(self, queryset, search_query):
        if search_query:
            sqs = SearchQuerySet().models(self.queryset.model).filter(content=search_query)
            object_ids = [result.pk for result in sqs]
            logger.debug(f"Search Query: {search_query}, Object IDs: {object_ids}")
            pk_field = self.queryset.model._meta.pk.name
            queryset = queryset.filter(**{f"{pk_field}__in": object_ids})
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        limit = self.request.query_params.get('limit', None)

        queryset = self.search_queryset(queryset, search_query)
        
        # Apply limit after all other query modifications
        if limit:
            queryset = queryset[:int(limit)]
        
        return queryset

@permission_classes([IsNotBlacklisted])
class DeviceViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer 
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        "device_id": ["exact"],
        "type": ["exact", "icontains"],
        "make": ["exact", "icontains"],
        "model": ["exact", "icontains"],
        "year_of_manufacture": ["exact", "gte", "lte"],
        "status": ["exact"],
        "operating_system": ["exact", "icontains"],
        "physical_condition": ["exact", "icontains"],
        "donor__name": ["exact", "icontains"],
        "location__name": ["exact", "icontains"],
        "assigned_user__username": ["exact", "icontains"],
    }
    search_fields = [
        "type", 
        "make", 
        "model", 
        "year_of_manufacture", 
        "status", 
        "operating_system", 
        "physical_condition", 
        "donor__name", 
        "location__name", 
        "assigned_user__username"
    ]
    ordering_fields = [
        "type", 
        "make", 
        "model", 
        "year_of_manufacture", 
        "status", 
        "operating_system", 
        "physical_condition", 
        "donor__name", 
        "location__name", 
        "assigned_user__username"
    ]
    ordering = ["type"]


@permission_classes([IsNotBlacklisted])
class WarehouseViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        "warehouse_number": ["exact"],
        "name": ["icontains"],
        "country": ["exact", "icontains"],
        "city": ["exact", "icontains"],
        "postal_code": ["exact"],
        "phone": ["exact"],
    }
    search_fields = [
        "name",
        "country",
        "city",
        "postal_code",
        "phone",
    ]
    ordering_fields = [
        "warehouse_number",
        "name",
        "country",
        "city",
        "postal_code",
        "phone",
    ]
    ordering = ["warehouse_number"]


@permission_classes([IsNotBlacklisted])
class DonorViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = {
        "name": ["icontains"],
        "contact_info": ["icontains"],
        "address": ["icontains"],
        "email": ["exact", "icontains"],
        "phone": ["exact"],
    }
    search_fields = [
        "name",
        "contact_info",
        "address",
        "email",
        "phone",
    ]
    ordering_fields = ["name", "email", "phone"]
    ordering = ["name"]



@permission_classes([IsNotBlacklisted])
class DeviceListCreate(generics.ListCreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@permission_classes([IsNotBlacklisted])
class DeviceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@permission_classes([IsNotBlacklisted])
class WarehouseListCreate(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


@permission_classes([IsNotBlacklisted])
class WarehouseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


@permission_classes([IsNotBlacklisted])
class DonorListCreate(generics.ListCreateAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


@permission_classes([IsNotBlacklisted])
class DonorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
