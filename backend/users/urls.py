"""
URL patterns for managing users through APIs.

Endpoints:
    Users:
        - {BaseURL}/users/:
            - GET: Retrieve a list of all users
            - POST: Create a new user.

        - {BaseURL}/users/<int:pk>/:
            - PUT: Update details of a specific user.
            - DELETE: Delete a specific user.
"""

from django.urls import path

from .views import UserListCreate, UserRetrieveUpdateDestroy

urlpatterns = [
    path("", UserListCreate.as_view(), name="user-list-create"),
    path("<int:pk>/", UserRetrieveUpdateDestroy.as_view(), name="user-detail"),
]
