from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend.authen.permissions import IsNotBlacklisted

from .mixins import BatchCreateMixin, BatchDeleteMixin, SearchAndLimitMixin
from .models import Device, Donor, Warehouse
from .pagination import CustomPagination
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer


@permission_classes([IsNotBlacklisted])
class DeviceViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
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
        "assigned_user__username",
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
        "assigned_user__username",
    ]
    ordering = ["type"]


@permission_classes([IsNotBlacklisted])
class WarehouseViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
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
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
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
        "mac_address",
        "mac_pro",
    ]
    ordering_fields = ["name", "email", "phone"]
    ordering = ["name"]


@permission_classes([IsNotBlacklisted])
class DeviceListCreate(BatchCreateMixin):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@permission_classes([IsNotBlacklisted])
class DeviceRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


@permission_classes([IsNotBlacklisted])
class WarehouseListCreate(BatchCreateMixin):
    def get_queryset(self):
        # Return the queryset you want to use
        return Warehouse.objects.all()

    serializer_class = WarehouseSerializer


@permission_classes([IsNotBlacklisted])
class WarehouseRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


@permission_classes([IsNotBlacklisted])
class DonorListCreate(BatchCreateMixin):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


@permission_classes([IsNotBlacklisted])
class DonorRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Donor.objects.all()
    serializer_class = DonorSerializer


@permission_classes([IsNotBlacklisted])
class WarehouseBatchDelete(BatchDeleteMixin):
    def get_queryset(self):
        return Warehouse.objects.all()


@permission_classes([IsNotBlacklisted])
class DonorBatchDelete(BatchDeleteMixin):
    def get_queryset(self):
        return Donor.objects.all()


@api_view(["POST"])
def device_batch_delete(request):
    data = request.data
    device_ids = data.get("device_ids")

    if device_ids is None:
        return Response(
            {"detail": "Request must contain a list of 'device_ids' to delete."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    devices = Device.objects.filter(pk__in=device_ids)
    devices.delete()

    return Response(
        {"detail": "Devices deleted successfully."}, status=status.HTTP_204_NO_CONTENT
    )
