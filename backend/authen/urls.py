from django.urls import path
from .views import AuthListCreate, AuthRetrieveUpdateDestroy, login

urlpatterns = [
    path('tokens/', AuthListCreate.as_view(), name='token-list-create'),
    path('tokens/<int:pk>/', AuthRetrieveUpdateDestroy.as_view(), name='token-retrieve-update-destroy'),
    path('login/', login, name='user-login'),
]
