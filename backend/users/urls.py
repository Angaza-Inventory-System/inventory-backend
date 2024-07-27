from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserCreate, UserViewSet, UpdateUserPermissionsView


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-permissions', UpdateUserPermissionsView, basename='user-permissions')

urlpatterns = [
    path('register/', UserCreate.as_view(), name='user-create'),
    path('', include(router.urls)),
]
