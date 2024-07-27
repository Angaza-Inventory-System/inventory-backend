"""
URL patterns for managing devices, warehouses, and donors through APIs.

Endpoints:
- Devices:
    - {{BaseURL}}/devices/:
        - GET: Retrieve a list of all devices with pagination and filtering.
        - POST: Create a new device.

    - {{BaseURL}}/devices/<uuid:pk>/:
        - PUT: Update details of a specific device.
        - DELETE: Delete a specific device.

    - {{BaseURL}}/devices/batch-delete/:
        - DELETE: Delete multiple devices at once.

- Warehouses:
    - {{BaseURL}}/warehouses/:
        - GET: Retrieve a list of all warehouses.
        - POST: Create a new warehouse.

    - {{BaseURL}}/warehouses/<int:pk>/:
        - PUT: Update details of a specific warehouse.
        - DELETE: Delete a specific warehouse.

    - {{BaseURL}}/warehouses/batch-delete/:
        - DELETE: Delete multiple warehouses at once.

- Donors:
    - {{BaseURL}}/donors/:
        - GET: Retrieve a list of all donors or create a new donor.
        - POST: Create a new donor.

    - {{BaseURL}}/donors/<int:pk>/:
        - PUT: Update details of a specific donor.
        - DELETE: Delete a specific donor.

    - {{BaseURL}}/donors/batch-delete/:
        - DELETE: Delete multiple donors at once.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DeviceListCreate,
    DeviceRetrieveUpdateDestroy,
    DeviceViewSet,
    DonorListCreate,
    DonorRetrieveUpdateDestroy,
    DonorViewSet,
    WarehouseListCreate,
    WarehouseRetrieveUpdateDestroy,
    WarehouseViewSet,
    batch_create,
    batch_delete,
)

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"donors", DonorViewSet, basename="donor")

urlpatterns = [
    path("", include(router.urls)),

    # Device URLs
    path("devices/", DeviceListCreate.as_view(), name="device-list-create"),
    path("devices/<uuid:pk>/", DeviceRetrieveUpdateDestroy.as_view(), name="device-detail"),


    # Warehouse URLs
    path("warehouses/", WarehouseListCreate.as_view(), name="warehouse-list-create"),
    path("warehouses/<int:pk>/", WarehouseRetrieveUpdateDestroy.as_view(), name="warehouse-detail"),


    # Donor URLs
    path("donors/", DonorListCreate.as_view(), name="donor-list-create"),
    path("donors/<int:pk>/", DonorRetrieveUpdateDestroy.as_view(), name="donor-detail"),


    # Batch URLs
    path("batch-create/", batch_create, name="batch-create"),
    path("batch-delete/", batch_delete, name="batch-delete"),
]
