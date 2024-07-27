from django_filters.rest_framework import DjangoFilterBackend
from django.apps import apps
from rest_framework import filters, generics, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from backend.authen.permissions import IsNotBlacklisted

from .mixins import SearchAndLimitMixin
from .models import Device, Donor, Warehouse
from .pagination import CustomPagination
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer
from .error_utils import handle_exception 

@permission_classes([IsNotBlacklisted])
class DeviceViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    serializer_class = DeviceSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
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
        "device_id",
        "serial_number",
        "mac_id",
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

@api_view(["DELETE"])
@permission_classes([IsNotBlacklisted])
def batch_delete(request):
    model_name = "devices." + request.query_params.get('model').capitalize()
    model = get_model(model_name)

    if model is None:
        return Response(
            {"error": "Invalid model specified."},
            status=status.HTTP_400_BAD_REQUEST
        )

    ids = validate_ids(request.data, "ids")
    if not ids:
        return Response(
            {"error": "Request must contain a list of 'ids' to delete."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        model.objects.filter(pk__in=ids).delete()
        return Response(
            {"message": "Records deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )
    except Exception as e:
        return handle_exception(e)

@api_view(["POST"])
@permission_classes([IsNotBlacklisted])
def batch_create(request):
    model_name = "devices." + request.query_params.get('model').capitalize()
    model = get_model(model_name)

    if model is None:
        return Response(
            {"error": f"Invalid model specified. {model_name}"},
            status=status.HTTP_400_BAD_REQUEST
        )

    data_list = request.data.get("objects")
    if not data_list or not isinstance(data_list, list):
        return Response(
            {"error": "Request must contain a list of objects to create."},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        for data in data_list:
            model.objects.create(**data)
        return Response(
            {"message": "Records created successfully."},
            status=status.HTTP_201_CREATED
        )
    except Exception as e:
        return handle_exception(e)

def validate_ids(data, id_key):
    ids = data.get(id_key)
    if not ids or not isinstance(ids, list):
        return False
    return ids

def generate_response(message, status_code):
    return Response({"detail": message}, status=status_code)

def get_model(model_path):
    try:
        app_label, model_name = model_path.rsplit('.', 1)
        return apps.get_model(app_label, model_name)
    except ValueError:
        return None
    except LookupError:
        return None