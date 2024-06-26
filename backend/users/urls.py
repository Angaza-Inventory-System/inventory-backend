"""
URL patterns for managing users through APIs.

Endpoints:
- /api/users/:
    - GET: Retrieve a list of all users or create a new user.
- /api/users/<int:pk>/:
    - GET: Retrieve details of a specific user.
    - PUT: Update details of a specific user.
    - DELETE: Delete a specific user.
"""

from django.urls import path
from .views import UserListCreate, UserRetrieveUpdateDestroy

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-detail'),
]
