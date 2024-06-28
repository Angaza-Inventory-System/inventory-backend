from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import User


class UserAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        url = reverse('user-list-create')
        data = {
            'username': 'testuser',
            'password': 'StrongPassword!123',
            'email': 'testuser@example.com',
            'role': 'Tester',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid_email(self):
        url = reverse('user-list-create')
        data = {
            'username': 'testuser',
            'password': 'StrongPassword!123',
            'email': 'invalidemail',  # Invalid email format
            'role': 'Tester',
            'first_name': 'Test',
            'last_name': 'User',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_user(self):
        user = User.objects.create(
            username='existinguser',
            password='StrongPassword!123',
            email='existinguser@example.com',
            role='Tester',
            first_name='Existing',
            last_name='User',
        )
        url = reverse('user-detail', kwargs={'pk': user.pk})
        updated_data = {
            'username': 'updateduser',
            'password': 'UpdatedPassword!456',
            'email': 'updateduser@example.com',
            'role': 'UpdatedRole',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user_invalid_password(self):
        user = User.objects.create(
            username='existinguser',
            password='StrongPassword!123',
            email='existinguser@example.com',
            role='Tester',
            first_name='Existing',
            last_name='User',
        )
        url = reverse('user-detail', kwargs={'pk': user.pk})
        updated_data = {
            'username': 'updateduser',
            'password': 'weak',  # Invalid password (less than 10 characters)
            'email': 'updateduser@example.com',
            'role': 'UpdatedRole',
            'first_name': 'Updated',
            'last_name': 'User',
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_user(self):
        user = User.objects.create(
            username='todeleteuser',
            password='StrongPassword!123',
            email='todeleteuser@example.com',
            role='Tester',
            first_name='To',
            last_name='Delete',
        )
        url = reverse('user-detail', kwargs={'pk': user.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_retrieve_user(self):
        user = User.objects.create(
            username='retrievableuser',
            password='StrongPassword!123',
            email='retrievableuser@example.com',
            role='Tester',
            first_name='Retrievable',
            last_name='User',
        )
        url = reverse('user-detail', kwargs={'pk': user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'retrievableuser')

