from rest_framework import filters, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from django_filters.rest_framework import DjangoFilterBackend

from backend.authen.permissions import IsNotBlacklisted
from backend.users.decorators import permission_required

from .models import Device, Donor, Warehouse
from .pagination import CustomPagination
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer


@permission_classes([IsNotBlacklisted])
class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
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
    ordering_fields = ["type", "make", "model", "year_of_manufacture", "status"]
    ordering = ["type"]

    @action(detail=False, methods=['get'])
    @permission_required(['readDevices'])
    def custom_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    @permission_required(['createDevices'])
    def custom_create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['put', 'patch'])
    @permission_required(['editDevices'])
    def custom_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['delete'])
    @permission_required(['deleteDevices'])
    def custom_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsNotBlacklisted])
class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "warehouse_number": ["exact"],
        "name": ["icontains"],
        "country": ["exact", "icontains"],
        "city": ["exact", "icontains"],
        "postal_code": ["exact"],
        "phone": ["exact"],
    }
    ordering_fields = [
        "warehouse_number",
        "name",
        "country",
        "city",
        "postal_code",
        "phone",
    ]
    ordering = ["warehouse_number"]

    @action(detail=False, methods=['get'])
    @permission_required(['manageWarehouses'])
    def custom_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    @permission_required(['manageWarehouses'])
    def custom_create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['put', 'patch'])
    @permission_required(['manageWarehouses'])
    def custom_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['delete'])
    @permission_required(['manageWarehouses'])
    def custom_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsNotBlacklisted])
class DonorViewSet(viewsets.ModelViewSet):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {
        "name": ["icontains"],
        "contact_info": ["icontains"],
        "address": ["icontains"],
        "email": ["exact", "icontains"],
        "phone": ["exact"],
    }
    ordering_fields = ["name", "email", "phone"]
    ordering = ["name"]

    @action(detail=False, methods=['get'])
    @permission_required(['manageDonors'])
    def custom_list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=False, methods=['post'])
    @permission_required(['manageDonors'])
    def custom_create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @action(detail=True, methods=['put', 'patch'])
    @permission_required(['manageDonors'])
    def custom_update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @action(detail=True, methods=['delete'])
    @permission_required(['manageDonors'])
    def custom_destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
