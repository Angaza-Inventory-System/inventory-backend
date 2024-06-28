import unittest
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from datetime import datetime, timedelta
from backend.users.models import User
from backend.authen.models import JWTToken


class JWTTokenTests(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='testuser@example.com')
        self.client = APIClient()

    def test_get_all_jwt_tokens(self):
        url = reverse('auth-list-create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_jwt_token(self):
        url = reverse('auth-list-create')
        expires_at = datetime.now() + timedelta(days=1)
        data = {
            'user': self.user.pk,
            'token': 'sample_token_value',
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at.isoformat(),
            'is_blacklisted': False
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('token_id', response.data)
        self.assertEqual(response.data['user'], self.user.pk)

    def test_get_jwt_token_details(self):
        token = JWTToken.objects.create(
            user=self.user,
            token='sample_token_value',
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=1),
            is_blacklisted=False
        )
        url = reverse('auth-detail', kwargs={'pk': token.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token_id'], token.pk)

    def test_update_jwt_token(self):
        token = JWTToken.objects.create(
            user=self.user,
            token='token_to_update',
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=1),
            is_blacklisted=False
        )
        url = reverse('auth-detail', kwargs={'pk': token.pk})
        expires_at = datetime.now() + timedelta(days=2)
        data = {
            'user': self.user.pk,
            'token': 'updated_token_value',
            'created_at': token.created_at.isoformat(),
            'expires_at': expires_at.isoformat(),
            'is_blacklisted': True
        }
        response = self.client.put(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token.refresh_from_db()
        self.assertEqual(token.token, 'updated_token_value')
        self.assertEqual(token.expires_at.date(), expires_at.date())
        self.assertTrue(token.is_blacklisted)

    def test_delete_jwt_token(self):
        token = JWTToken.objects.create(
            user=self.user,
            token='token_to_delete',
            created_at=datetime.now(),
            expires_at=datetime.now() + timedelta(days=1),
            is_blacklisted=False
        )
        url = reverse('auth-detail', kwargs={'pk': token.pk})
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(JWTToken.objects.filter(pk=token.pk).exists())


if __name__ == '__main__':
    unittest.main()
