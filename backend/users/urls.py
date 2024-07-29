from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UpdateUserPermissionsView, UserCreate, UserViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(
    r"user-permissions", UpdateUserPermissionsView, basename="user-permissions"
)

urlpatterns = [
    path("", include(router.urls)),  # This will include all the routes from the router.
    path("register/", UserCreate.as_view(), name="user-create"),
    path(
        "user-permissions/<str:username>/",
        UpdateUserPermissionsView.as_view(
            {"get": "retrieve_permissions", "patch": "update_permissions"}
        ),
        name="user-permissions-detail",
    ),
]
