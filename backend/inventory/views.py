from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend.authen.permissions import IsBlacklisted
from backend.inventory.helpers.batch_operations import get_model, validate_ids
from backend.inventory.helpers.mock_data import (
    generate_mock_device,
    generate_mock_donor,
    generate_mock_warehouse,
)
from backend.users.decorators import permission_required

from .error_utils import handle_exception
from .mixins import SearchAndLimitMixin
from .models import Device, Donor, Location, Shipment, User
from .pagination import CustomPagination
from .serializers import DeviceSerializer, DonorSerializer, LocationSerializer, ShipmentSerializer
from .base_viewset import PermissionRequiredViewSet


class DeviceViewSet(PermissionRequiredViewSet):
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
        "created_by__username": ["exact", "icontains"],
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
        "created_by__username",
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
        "created_by__username",
    ]
    ordering = ["type"]
    permission_required_map = {
        'get': ['readDevices'],
        'post': ['createDevices'],
        'put': ['editDevices'],
        'patch': ['editDevices'],
        'delete': ['deleteDevices'],
    }

class LocationViewSet(PermissionRequiredViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
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
    permission_required_map = {
        'get': ['manageWarehouses'],
        'post': ['manageWarehouses'],
        'put': ['manageWarehouses'],
        'patch': ['manageWarehouses'],
        'delete': ['manageWarehouses'],
    }

class DonorViewSet(PermissionRequiredViewSet):
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
    ]
    ordering_fields = ["name", "email", "phone"]
    ordering = ["name"]
    permission_required_map = {
        'get': ['manageDonors'],
        'post': ['manageDonors'],
        'put': ['manageDonors'],
        'patch': ['manageDonors'],
        'delete': ['manageDonors'],
    }

class ShipmentViewSet(PermissionRequiredViewSet):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_fields = {
        "shipping_id": ["exact"],
        "destination__name": ["exact", "icontains"],
        "arrived": ["exact"],
        "date_shipped": ["exact", "gte", "lte"],
        "date_delivered": ["exact", "gte", "lte"],
        "tracking_identifier": ["icontains"],
    }
    search_fields = [
        "tracking_identifier",
        "destination__name",
    ]
    ordering_fields = [
        "shipping_id",
        "date_shipped",
        "date_delivered",
        "tracking_identifier",
    ]
    ordering = ["date_shipped"]
    permission_required_map = {
        'get': ['manageShipments'],
        'post': ['manageShipments'],
        'put': ['manageShipments'],
        'patch': ['manageShipments'],
        'delete': ['manageShipments'],
    }

@api_view(["PATCH", "DELETE"])
@permission_classes([IsBlacklisted])
@permission_required('batchUploadDevices')
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
        num_warehouses = request.data.get("num_warehouses", 5)
        num_donors = request.data.get("num_donors", 10)
        num_devices = request.data.get("num_devices", 50)

        # Generate mock data
        new_warehouses = generate_mock_warehouse(num_warehouses)
        new_donors = generate_mock_donor(num_donors)

        # Create warehouse and donor objects
        created_warehouses = Location.objects.bulk_create(
            [Location(**w) for w in new_warehouses]
        )
        created_donors = Donor.objects.bulk_create([Donor(**d) for d in new_donors])

        # Get all warehouses, donors, and users for device creation
        all_warehouses = list(Location.objects.all())
        all_donors = list(Donor.objects.all())
        all_users = list(User.objects.all())

        # Generate and create device objects
        new_devices = generate_mock_device(
            num_devices, all_warehouses, all_donors, all_users
        )
        created_devices = Device.objects.bulk_create([Device(**d) for d in new_devices])

        return Response(
            {
                "message": "Mock data generated successfully",
                "warehouses_created": len(created_warehouses),
                "donors_created": len(created_donors),
                "devices_created": len(created_devices),
            },
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return handle_exception(e)
