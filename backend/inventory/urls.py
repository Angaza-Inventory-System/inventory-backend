from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    DeviceViewSet,
    DonorViewSet,
    LocationViewSet,
    batch_operations,
    generate_mock_data,
)

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"locations", LocationViewSet, basename="location")
router.register(r"donors", DonorViewSet, basename="donor")

urlpatterns = [
    path("", include(router.urls)),
    # Batch Actions URL
    path("batch/", batch_operations, name="batch-operations"),
    # Mock Data Generation URL
    path("generate-mock-data/", generate_mock_data, name="generate-mock-data"),
]
