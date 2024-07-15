"""
URL patterns for managing users through APIs.

Endpoints:
    Users:
        - {{BaseURL}}/users/:
            - GET: Retrieve a list of all users

        - {{BaseURL}}/users/register/:
            - POST: Create a new user.

        - {{BaseURL}}/users/<int:pk>/:
            - PUT: Update details of a specific user.
            - DELETE: Delete a specific user.
"""

from django.urls import path

from .views import UserCreate, UserList, UserRetrieveUpdateDestroy, UpdateUserPermissionsView, UserPermissionsView

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("register/", UserCreate.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveUpdateDestroy.as_view(), name="user-detail"),
    path("<str:username>/permissions/", UserPermissionsView.as_view(), name='get_user_permissions'),
    path("<str:username>/permissions/update/", UpdateUserPermissionsView.as_view(), name='update_user_permissions'),
]
