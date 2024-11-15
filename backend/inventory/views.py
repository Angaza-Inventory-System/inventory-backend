from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend.authen.permissions import IsBlacklisted
from backend.inventory.helpers.batch_operations import get_model, validate_ids
from backend.inventory.helpers.mock_data import create_mock_data
from backend.users.decorators import permission_required

from .error_utils import handle_exception
from .mixins import SearchAndLimitMixin
from .models import Device, Donor, Location, User
from .pagination import CustomPagination
from .serializers import DeviceSerializer, DonorSerializer, WarehouseSerializer


@permission_classes([IsBlacklisted])
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
        "operating_system": ["exact", "icontains"],
        "physical_condition": ["exact", "icontains"],
        "donor__name": ["exact", "icontains"],
        "start_location__name": ["exact", "icontains"],
        "end_location__name": ["exact", "icontains"],
        "created_by__username": ["exact", "icontains"],
    }
    search_fields = [
        "device_id",
        "type",
        "make",
        "model",
        "year_of_manufacture",
        "operating_system",
        "physical_condition",
        "donor__name",
        "start_location__name",
        "end_location__name",
        "created_by__username",
    ]
    ordering_fields = [
        "type",
        "make",
        "model",
        "year_of_manufacture",
        "operating_system",
        "physical_condition",
        "donor__name",
        "start_location__name",
        "end_location__name",
        "created_by__username",
    ]
    ordering = ["type"]

    @permission_required(["readDevices"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(["createDevices"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required(["editDevices"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(["editDevices"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @permission_required(["deleteDevices"])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsBlacklisted])
class LocationViewSet(SearchAndLimitMixin, viewsets.ModelViewSet):
    queryset = Location.objects.all()
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
        "location_id": ["exact"],
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
        "location_id",
        "name",
        "country",
        "city",
        "postal_code",
        "phone",
    ]
    ordering = ["location_id"]

    @permission_required(["manageWarehouses"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(["manageWarehouses"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required(["manageWarehouses"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(["manageWarehouses"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @permission_required(["manageWarehouses"])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@permission_classes([IsBlacklisted])
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

    @permission_required(["manageDonors"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @permission_required(["manageDonors"])
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @permission_required(["manageDonors"])
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @permission_required(["manageDonors"])
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @permission_required(["manageDonors"])
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.perform_destroy(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH", "DELETE"])
@permission_classes([IsBlacklisted])
def batch_operations(request):
    model_name = "devices." + request.query_params.get("model").capitalize()
    model = get_model(model_name)

    if model is None:
        return Response(
            {"error": f"Invalid model specified. {model_name}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if request.method == "PATCH":
        return batch_edit(request, model)
    elif request.method == "DELETE":
        return batch_delete(request, model)


def batch_edit(request, model):
    data_list = request.data.get("objects")
    if not data_list or not isinstance(data_list, list):
        return Response(
            {"error": "Request must contain a list of objects to edit."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        updated_count = 0
        for data in data_list:
            if "id" not in data:
                return Response(
                    {"error": "Each object must contain an 'id' field."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            obj_id = data.pop("id")
            obj = model.objects.filter(pk=obj_id).first()
            if obj:
                for key, value in data.items():
                    setattr(obj, key, value)
                obj.save()
                updated_count += 1

        return Response(
            {"message": f"{updated_count} records updated successfully."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return handle_exception(e)


def batch_delete(request, model):
    ids = validate_ids(request.data, "ids")
    if not ids:
        return Response(
            {"error": "Request must contain a list of 'ids' to delete."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        deleted_count, _ = model.objects.filter(pk__in=ids).delete()
        return Response(
            {"message": f"{deleted_count} records deleted successfully."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        return handle_exception(e)


@api_view(["POST"])
def generate_mock_data(request):
    try:
        num_locations = request.data.get("num_locations", 5)
        num_donors = request.data.get("num_donors", 10)
        num_devices = request.data.get("num_devices", 50)
        num_shipping = request.data.get("num_shipping", 20)

        # Generate mock data
        result = create_mock_data(
            num_locations=num_locations,
            num_donors=num_donors,
            num_devices=num_devices,
            num_shipping=num_shipping,
        )

        return Response(
            {"message": "Mock data generated successfully", **result},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return handle_exception(e)
