"""
URL routing for user management in the API.

This module sets up the URL routing for user management using Django REST Framework's `DefaultRouter`.
It includes endpoints for creating and updating user information, as well as managing user permissions.

Endpoints:

1. **User Endpoints**
   - `GET {{base_url}}/users/users/`: List all users.
   - `POST {{base_url}}/users/users/`: Create a new user.
   - `GET {{base_url}}/users/users/{id}/`: Retrieve a specific user.
   - `PUT {{base_url}}/users/users/{id}/`: Update a specific user.
   - `PATCH {{base_url}}/users/users/{id}/`: Partially update a specific user.
   - `DELETE {{base_url}}/users/users/{id}/`: Delete a specific user.

2. **User Registration**
   - `POST {{base_url}}/users/register/`: Register a new user. This endpoint is for user creation and registration.

3. **User Password Update**
   - `PATCH {{base_url}}/users/password/`: Update the password of the currently authenticated user.

4. **User Permissions Endpoints**
   - `GET {{base_url}}/users/user-permissions/<str:username>/`: Retrieve permissions for a specific user by username.
   - `PATCH {{base_url}}/users/user-permissions/<str:username>/`: Partially update permissions for a specific user by username.
   - `PUT {{base_url}}/users/user-permissions/<str:username>/`: Update all permissions for a specific user by username.
   - `DELETE {{base_url}}/users/user-permissions/<str:username>/`: Delete a specific user's permissions by username.
   - `DELETE {{base_url}}/users/user-permissions/<str:username>/clear/`: Remove all permissions for a specific user by username.

Router Configuration:
- The `DefaultRouter` generates routes for CRUD operations on:
  - `UserViewSet`
  - `UserPermissionsViewSet`

The `urlpatterns` list includes both router-generated URLs and custom URLs for user registration, password updates, and managing user permissions.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    UserCreate,
    UserPasswordUpdateView,
    UserPermissionsViewSet,
    UserViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(
    r"user-permissions", UserPermissionsViewSet, basename="user-permissions"
)

urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserCreate.as_view(), name="user-create"),
    path("password/", UserPasswordUpdateView.as_view(), name="user-password-update"),
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
