"""
URL patterns for user authentication through API login.

Endpoints:
    User Login:
        - {{BaseURL}}/authen/login/:
            - POST: Authenticate a user and return a JWT token.
"""

from django.urls import path

from .views import login

urlpatterns = [
    path("login/", login, name="user-login"),
]
