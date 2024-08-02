"""
URL routing for the inventory management API.

This module sets up the URL routing for the inventory management API using Django REST Framework's `DefaultRouter`.
It includes endpoints for managing devices, locations, donors, and shipments, as well as additional endpoints for batch operations and generating mock data.

Endpoints:

1. **Device Endpoints**
   - `GET {{base_url}}/inventory/devices/`: List all devices.
   - `POST {{base_url}}/inventory/devices/`: Create a new device.
   - `GET {{base_url}}/inventory/devices/{id}/`: Retrieve a specific device.
   - `PUT {{base_url}}/inventory/devices/{id}/`: Update a specific device.
   - `PATCH {{base_url}}/inventory/devices/{id}/`: Partially update a specific device.
   - `DELETE {{base_url}}/inventory/devices/{id}/`: Delete a specific device.

2. **Location Endpoints**
   - `GET {{base_url}}/inventory/locations/`: List all locations.
   - `POST {{base_url}}/inventory/locations/`: Create a new location.
   - `GET {{base_url}}/inventory/locations/{id}/`: Retrieve a specific location.
   - `PUT {{base_url}}/inventory/locations/{id}/`: Update a specific location.
   - `PATCH {{base_url}}/inventory/locations/{id}/`: Partially update a specific location.
   - `DELETE {{base_url}}/inventory/locations/{id}/`: Delete a specific location.

3. **Donor Endpoints**
   - `GET {{base_url}}/inventory/donors/`: List all donors.
   - `POST {{base_url}}/inventory/donors/`: Create a new donor.
   - `GET {{base_url}}/inventory/donors/{id}/`: Retrieve a specific donor.
   - `PUT {{base_url}}/inventory/donors/{id}/`: Update a specific donor.
   - `PATCH {{base_url}}/inventory/donors/{id}/`: Partially update a specific donor.
   - `DELETE {{base_url}}/inventory/donors/{id}/`: Delete a specific donor.

4. **Shipment Endpoints**
   - `GET {{base_url}}/inventory/shipments/`: List all shipments.
   - `POST {{base_url}}/inventory/shipments/`: Create a new shipment.
   - `GET {{base_url}}/inventory/shipments/{id}/`: Retrieve a specific shipment.
   - `PUT {{base_url}}/inventory/shipments/{id}/`: Update a specific shipment.
   - `PATCH {{base_url}}/inventory/shipments/{id}/`: Partially update a specific shipment.
   - `DELETE {{base_url}}/inventory/shipments/{id}/`: Delete a specific shipment.

5. **Batch Operations**
   - `POST {{base_url}}/inventory/batch/`: Perform batch operations (create, update, or delete) on records for devices, donors, locations, or shipments.

6. **Mock Data Generation**
   - `POST {{base_url}}/inventory/generate-mock-data/`: Populate the database with sample data for testing purposes.

Router Configuration:
- The `DefaultRouter` generates routes for CRUD operations on:
  - `DeviceViewSet`
  - `LocationViewSet`
  - `DonorViewSet`
  - `ShipmentViewSet`

The `urlpatterns` list includes both router-generated URLs and custom URLs for batch operations and mock data generation.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DeviceViewSet,
    DonorViewSet,
    LocationViewSet,
    ShipmentViewSet,
    batch_operations,
    generate_mock_data,
)

router = DefaultRouter()
router.register(r'devices', DeviceViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'donors', DonorViewSet)
router.register(r'shipments', ShipmentViewSet)

urlpatterns = [
    path("", include(router.urls)),
    # Batch Actions URL
    path("batch/", batch_operations, name="batch-operations"),
    # Mock Data Generation URL
    path("generate-mock-data/", generate_mock_data, name="generate-mock-data"),
]
