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

from .views import UserList, UserCreate, UserRetrieveUpdateDestroy

urlpatterns = [
    path("", UserList.as_view(), name="user-list"),
    path("register/", UserCreate.as_view(), name="user-create"),
    path("<int:pk>/", UserRetrieveUpdateDestroy.as_view(), name="user-detail"),
]
