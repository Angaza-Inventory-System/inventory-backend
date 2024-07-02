"""
Unit tests for JWTToken CRUD operations via API endpoints.

Endpoints:
- {BaseURL}/auth/:
    - GET: Retrieve a list of all authentication entries or create a new entry.
- {BaseURL}/auth/<int:pk>/:
    - GET: Retrieve details of a specific authentication entry.
    - PUT: Update details of a specific authentication entry.
    - DELETE: Delete a specific authentication entry.

Test Cases:
- test_get_all_jwt_tokens: Tests GET request to retrieve all JWT tokens.
- test_create_jwt_token: Tests POST request to create a new JWT token.
- test_get_jwt_token_details: Tests GET request to retrieve details of a JWT token.
- test_update_jwt_token: Tests PUT request to update details of a JWT token.
- test_delete_jwt_token: Tests DELETE request to delete a JWT token.
"""

import unittest
from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from backend.authen.models import JWTToken
from backend.users.models import User


class JWTTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", email="testuser@example.com"
        )
        self.client = APIClient()

    def test_get_all_jwt_tokens(self):
        url = reverse("auth-list-create")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_jwt_token(self):
        url = reverse("auth-list-create")
        expires_at = datetime.now() + timedelta(days=1)
        data = {
            "user": self.user.pk,
            "token": "sample_token_value",
            "created_at": datetime.now().isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_blacklisted": False,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("token_id", response.data)
        self.assertEqual(response.data["user"], self.user.pk)

    def test_get_jwt_token_details(self):
        token = JWTToken.objects.create(
            user=self.user,
            token="sample_token_value",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=1),
            is_blacklisted=False,
        )
        url = reverse("auth-detail", kwargs={"pk": token.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["token_id"], token.pk)

    def test_update_jwt_token(self):
        token = JWTToken.objects.create(
            user=self.user,
            token="token_to_update",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=1),
            is_blacklisted=False,
        )
        url = reverse("auth-detail", kwargs={"pk": token.pk})
        expires_at = datetime.now() + timedelta(days=2)
        data = {
            "user": self.user.pk,
            "token": "updated_token_value",
            "created_at": token.created_at.isoformat(),
            "expires_at": expires_at.isoformat(),
            "is_blacklisted": True,
        }
        response = self.client.put(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token.refresh_from_db()
        self.assertEqual(token.token, "updated_token_value")
        self.assertEqual(token.expires_at.date(), expires_at.date())
        self.assertTrue(token.is_blacklisted)

    def test_delete_jwt_token(self):
        token = JWTToken.objects.create(
            user=self.user,
            token="token_to_delete",
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=1),
            is_blacklisted=False,
        )
        url = reverse("auth-detail", kwargs={"pk": token.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JWTToken.objects.filter(pk=token.pk).exists())


if __name__ == "__main__":
    unittest.main()
