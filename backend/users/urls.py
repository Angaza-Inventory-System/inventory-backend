from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UserCreate, UserPermissionsViewSet, UserViewSet, UserPasswordUpdateView

# Initialize the router
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(
    r"user-permissions", UserPermissionsViewSet, basename="user-permissions"
)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreate.as_view(), name="user-create"),
    path('password/', UserPasswordUpdateView.as_view(), name='user-password-update'),
    path(
        "user-permissions/<str:username>/",
        UserPermissionsViewSet.as_view(
            {
                "get": "retrieve",
                "patch": "partial_update",
                "put": "update",
                "delete": "destroy",
            }
        ),
        name="user-permissions-detail",
    ),
    path(
        "user-permissions/<str:username>/clear/",
        UserPermissionsViewSet.as_view({"delete": "delete_all_permissions"}),
        name="user-permissions-clear",
    ),
]
