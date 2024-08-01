import random
from datetime import timedelta

from django.apps import apps
from django.db.models import Max
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from backend.authen.permissions import IsBlacklisted
from backend.users.decorators import permission_required

from .error_utils import handle_exception
from .mixins import SearchAndLimitMixin
from .models import Device, Donor, User, Warehouse
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


@api_view(["DELETE"])
@permission_classes([IsBlacklisted])
def batch_delete(request):
    model_name = "devices." + request.query_params.get("model").capitalize()
    model = get_model(model_name)

    if model is None:
        return Response(
            {"error": "Invalid model specified."}, status=status.HTTP_400_BAD_REQUEST
        )

    ids = validate_ids(request.data, "ids")
    if not ids:
        return Response(
            {"error": "Request must contain a list of 'ids' to delete."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        model.objects.filter(pk__in=ids).delete()
        return Response(
            {"message": "Records deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
    except Exception as e:
        return handle_exception(e)


@api_view(["POST"])
@permission_classes([IsBlacklisted])
def batch_create(request):
    model_name = "devices." + request.query_params.get("model").capitalize()
    model = get_model(model_name)

    if model is None:
        return Response(
            {"error": f"Invalid model specified. {model_name}"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    data_list = request.data.get("objects")
    if not data_list or not isinstance(data_list, list):
        return Response(
            {"error": "Request must contain a list of objects to create."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        for data in data_list:
            model.objects.create(**data)
        return Response(
            {"message": "Records created successfully."}, status=status.HTTP_201_CREATED
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
        app_label, model_name = model_path.rsplit(".", 1)
        return apps.get_model(app_label, model_name)
    except ValueError:
        return None
    except LookupError:
        return None


def generate_mock_warehouse(num_warehouses):
    warehouses = []
    # Get the maximum existing warehouse number
    max_warehouse_number = (
        Warehouse.objects.aggregate(Max("warehouse_number"))["warehouse_number__max"]
        or 0
    )

    for i in range(num_warehouses):
        warehouse = {
            "warehouse_number": max_warehouse_number + i + 1,
            "name": f"Warehouse {max_warehouse_number + i + 1}",
            "country": random.choice(["USA", "Canada", "UK", "Germany", "France"]),
            "city": f"City {max_warehouse_number + i + 1}",
            "postal_code": f"{random.randint(10000, 99999)}",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        }
        warehouses.append(warehouse)
    return warehouses


def generate_mock_donor(num_donors):
    donors = []
    # Get the count of existing donors
    existing_donors_count = Donor.objects.count()

    for i in range(num_donors):
        donor = {
            "name": f"Donor {existing_donors_count + i + 1}",
            "contact_info": f"Contact {existing_donors_count + i + 1}",
            "address": f"Address {existing_donors_count + i + 1}, City {existing_donors_count + i + 1}",
            "email": f"donor{existing_donors_count + i + 1}@example.com",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        }
        donors.append(donor)
    return donors


def generate_mock_device(num_devices, warehouses, donors, users):
    devices = []
    # Get the count of existing devices
    existing_devices_count = Device.objects.count()

    for i in range(num_devices):
        device = {
            "type": random.choice(["Laptop", "Desktop", "Tablet", "Smartphone"]),
            "make": random.choice(["Dell", "HP", "Lenovo", "Apple", "Samsung"]),
            "model": f"Model {existing_devices_count + i + 1}",
            "serial_number": f"SN-{existing_devices_count + i + 1}-{random.randint(10000, 99999)}",
            "mac_id": f"MAC-{existing_devices_count + i + 1}-{random.randint(100000, 999999)}",
            "year_of_manufacture": random.randint(2015, 2023),
            "shipment_date": (
                timezone.now() - timedelta(days=random.randint(1, 365))
            ).date(),
            "date_received": (
                timezone.now() - timedelta(days=random.randint(1, 30))
            ).date(),
            "received_by": random.choice(users) if users else None,
            "physical_condition": random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "specifications": f"Specs for Device {existing_devices_count + i + 1}",
            "operating_system": random.choice(
                ["Windows 10", "macOS", "Linux", "Android", "iOS"]
            ),
            "accessories": f"Accessories for Device {existing_devices_count + i + 1}",
            "donor": random.choice(donors) if donors else None,
            "date_of_donation": (
                timezone.now() - timedelta(days=random.randint(1, 180))
            ).date(),
            "value": round(random.uniform(100, 1000), 2),
            "location": random.choice(warehouses) if warehouses else None,
            "created_by": random.choice(users) if users else None,
            "status": random.choice(["Available", "In Use", "Under Repair", "Retired"]),
            "distributor": f"Distributor {existing_devices_count + i + 1}",
            "warranty_service_info": f"Warranty info for Device {existing_devices_count + i + 1}",
            "notes": f"Notes for Device {existing_devices_count + i + 1}",
        }
        devices.append(device)
    return devices


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
        created_warehouses = Warehouse.objects.bulk_create(
            [Warehouse(**w) for w in new_warehouses]
        )
        created_donors = Donor.objects.bulk_create([Donor(**d) for d in new_donors])

        # Get all warehouses, donors, and users for device creation
        all_warehouses = list(Warehouse.objects.all())
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
