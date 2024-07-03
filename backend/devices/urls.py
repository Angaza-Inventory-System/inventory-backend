"""
URL patterns for managing devices, warehouses, and donors through APIs.

Endpoints:
    Devices:
        - {BaseURL}/devices/devices/:
            - GET: Retrieve a list of all devices WITH pagination and filtering 
            - POST: Create a new device.

        - {BaseURL}/devices/devices/<uuid:pk>/:
            - PUT: Update details of a specific device.
            - DELETE: Delete a specific device.

    Warehouses:
        - {BaseURL}/devices/warehouses/:
            - GET: Retrieve a list of all warehouses.
            - POST: Create a new warehouse.

        - {BaseURL}/devices/warehouses/<int:pk>/:
            - PUT: Update details of a specific warehouse.
            - DELETE: Delete a specific warehouse.

    Donors:
        - {BaseURL}/devices/donors/:
            - GET: Retrieve a list of all donors or create a new donor.
            - POST: Create a new device.

        - {BaseURL}/devices/donors/<int:pk>/:
            - PUT: Update details of a specific donor.
            - DELETE: Delete a specific donor.
"""

from django.urls import path, include
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
router.register(r'devices', DeviceViewSet, basename='device')
router.register(r'warehouses', WarehouseViewSet, basename='warehouse')
router.register(r'donors', DonorViewSet, basename='donor')

urlpatterns = [
    path('', include(router.urls)),
    path("devices/", DeviceListCreate.as_view(), name="device-list-create"),
    path("devices/<uuid:pk>/", DeviceRetrieveUpdateDestroy.as_view(), name="device-detail"),
    path("warehouses/", WarehouseListCreate.as_view(), name="warehouse-list-create"),
    path("warehouses/<int:pk>/", WarehouseRetrieveUpdateDestroy.as_view(), name="warehouse-detail"),
    path("donors/", DonorListCreate.as_view(), name="donor-list-create"),
    path("donors/<int:pk>/", DonorRetrieveUpdateDestroy.as_view(), name="donor-detail"),
]
