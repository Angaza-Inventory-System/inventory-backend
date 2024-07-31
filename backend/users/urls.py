from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import UpdateUserPermissionsView, UserCreate, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(
    r"user-permissions", UpdateUserPermissionsView, basename="user-permissions"
)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreate.as_view(), name="user-create"),
    path(
        "user-permissions/<str:username>/",
        UpdateUserPermissionsView.as_view(
            {
                "get": "get",
                "put": "replace_permissions",
                "patch": "add_permissions",
                "delete": "remove_permissions",
            }
        ),
        name="user-permissions-detail",
    ),
    path(
        "user-permissions/<str:username>/clear/",
        UpdateUserPermissionsView.as_view({"delete": "delete_all_permissions"}),
        name="user-permissions-clear",
    ),
]
