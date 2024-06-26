from django.urls import path
from .views import DeviceListCreate, DeviceRetrieveUpdateDestroy

urlpatterns = [
    path('devices/', DeviceListCreate.as_view(), name='device-list-create'),
    path('devices/<uuid:pk>/', DeviceRetrieveUpdateDestroy.as_view(), name='device-detail'),
]
