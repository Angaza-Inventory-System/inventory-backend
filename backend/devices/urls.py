from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DeviceViewSet, WarehouseViewSet, DonorViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"warehouses", WarehouseViewSet, basename="warehouse")
router.register(r"donors", DonorViewSet, basename="donor")

urlpatterns = [
    path("", include(router.urls)),
]
