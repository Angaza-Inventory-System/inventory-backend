from django.urls import include, path

urlpatterns = [
    path("auth/", include("angaza_inventory_system.auth.urls")),
    path("devices/", include("angaza_inventory_system.devices.urls")),
    path("users/", include("angaza_inventory_system.users.urls")),
]
