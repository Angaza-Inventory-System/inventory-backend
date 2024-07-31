from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeviceViewSet, DonorViewSet, WarehouseViewSet, batch_create, batch_delete, generate_mock_data,

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"donors", DonorViewSet, basename="donor")

urlpatterns = [
    path("", include(router.urls)),
    # Batch URLs
    path("batch-create/", batch_create, name="batch-create"),
    path("batch-delete/", batch_delete, name="batch-delete"),
    # Mock Data Generation URL
    path("generate-mock-data/", generate_mock_data, name="generate-mock-data"),
]
