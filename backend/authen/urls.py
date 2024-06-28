"""
URL patterns for managing authentication through APIs.

Endpoints:
- /api/auth/:
    - GET: Retrieve a list of all authentication entries or create a new entry.
- /api/auth/<int:pk>/:
    - GET: Retrieve details of a specific authentication entry.
    - PUT: Update details of a specific authentication entry.
    - DELETE: Delete a specific authentication entry.
"""

from django.urls import path
from .views import AuthListCreate, AuthRetrieveUpdateDestroy

urlpatterns = [
    path('auth/', AuthListCreate.as_view(), name='auth-list-create'),
    path('auth/<int:pk>/', AuthRetrieveUpdateDestroy.as_view(), name='auth-detail'),
]
