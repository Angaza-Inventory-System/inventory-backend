# devices/urls.py
from django.urls import path
from .views import UserListCreate, UserRetrieveUpdateDestroy

urlpatterns = [
    path('users/', UserListCreate.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroy.as_view(), name='user-detail'),
]
