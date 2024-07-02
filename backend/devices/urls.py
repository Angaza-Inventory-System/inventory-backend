"""
URL patterns for managing devices, warehouses, and donors through APIs.

Endpoints:
- /api/devices/:
    - GET: Retrieve a list of all devices or create a new device.
- /api/devices/<uuid:pk>/:
    - GET: Retrieve details of a specific device.
    - PUT: Update details of a specific device.
    - DELETE: Delete a specific device.
- /api/warehouses/:
    - GET: Retrieve a list of all warehouses or create a new warehouse.
- /api/warehouses/<int:pk>/:
    - GET: Retrieve details of a specific warehouse.
    - PUT: Update details of a specific warehouse.
    - DELETE: Delete a specific warehouse.
- /api/donors/:
    - GET: Retrieve a list of all donors or create a new donor.
- /api/donors/<int:pk>/:
    - GET: Retrieve details of a specific donor.
    - PUT: Update details of a specific donor.
    - DELETE: Delete a specific donor.
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
)

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"donors", DonorViewSet, basename="donor")

urlpatterns = [
    path("", include(router.urls)),
    path("devices/", DeviceListCreate.as_view(), name="device-list-create"),
    path(
        "devices/<uuid:pk>/",
        DeviceRetrieveUpdateDestroy.as_view(),
        name="device-detail",
    ),
    path("warehouses/", WarehouseListCreate.as_view(), name="warehouse-list-create"),
    path(
        "warehouses/<int:pk>/",
        WarehouseRetrieveUpdateDestroy.as_view(),
        name="warehouse-detail",
    ),
    path("donors/", DonorListCreate.as_view(), name="donor-list-create"),
    path("donors/<int:pk>/", DonorRetrieveUpdateDestroy.as_view(), name="donor-detail"),
]
