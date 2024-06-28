import datetime
import random

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from backend.devices.models import Device, Donor, Warehouse
from backend.users.models import User


class CreateEntitiesTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_users()
        self.create_donors()
        self.create_warehouses()
        self.create_devices()

    def create_users(self):
        for i in range(1, 11):
            url = reverse("user-list-create")
            data = {
                "username": f"testuser{i}",
                "password": "StrongPassword!123",
                "email": f"testuser{i}@example.com",
                "role": "Tester",
                "first_name": f"Test{i}",
                "last_name": f"User{i}",
            }
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_donors(self):
        for i in range(1, 11):
            url = reverse("donor-list-create")
            data = {
                "name": f"Donor Name {i}",
                "contact_info": f"Contact Info {i}",
                "address": f"Donor Address {i}",
                "email": f"donor{i}@example.com",
                "phone": f"12345678{i}",
            }
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_warehouses(self):
        for i in range(1, 11):
            url = reverse("warehouse-list-create")
            data = {
                "warehouse_number": i,
                "name": f"Warehouse {i}",
                "country": "Country",
                "city": "City",
                "postal_code": "12345",
                "phone": f"12345678{i}",
            }
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_devices(self):
        users = User.objects.all()
        donors = Donor.objects.all()
        warehouses = Warehouse.objects.all()

        for i in range(1, 5):
            user_received_by = random.choice(users)
            user_assigned_to = random.choice(users)
            donor = random.choice(donors)
            warehouse = random.choice(warehouses)

            url = reverse("device-list-create")
            data = {
                "type": f"Test Type {i}",
                "make": f"Test Make {i}",
                "model": f"Test Model {i}",
                "serial_number": f"SN{i}12345",  # Unique
                "mac_id": f"MAC{i}12345",  # Unique
                "year_of_manufacture": 2023,
                "shipment_date": datetime.date.today(),
                "date_received": datetime.date.today(),
                "received_by": user_received_by.pk,
                "physical_condition": "Good",
                "specifications": f"Test specifications {i}",
                "operating_system": "Windows 10",
                "accessories": "None",
                "donor": donor.pk,
                "date_of_donation": datetime.date.today(),
                "value": "1000.00",
                "location": warehouse.pk,
                "assigned_user": user_assigned_to.pk,
                "status": "Available",
                "distributor": f"Test Distributor {i}",
                "warranty_service_info": "Warranty info",
                "notes": f"Test notes {i}",
            }
            response = self.client.post(url, data, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_devices(self):
        url = reverse("device-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_warehouses(self):
        url = reverse("warehouse-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_donors(self):
        url = reverse("donor-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_device(self):
        device = Device.objects.first()
        self.assertIsNotNone(device, "No device found in the database.")
        url = reverse("device-detail", kwargs={"pk": device.pk})
        data = {
            "type": "Updated Type",
            "make": "Updated Make",
            "model": "Updated Model",
            "serial_number": "Updated SN12345",
            "mac_id": "Updated MAC12345",
            "year_of_manufacture": 2024,
            "shipment_date": datetime.date.today(),
            "date_received": datetime.date.today(),
            "received_by": random.choice(User.objects.all()).pk,
            "physical_condition": "Updated Condition",
            "specifications": "Updated Specifications",
            "operating_system": "Updated OS",
            "accessories": "Updated Accessories",
            "donor": random.choice(Donor.objects.all()).pk,
            "date_of_donation": datetime.date.today(),
            "value": "2000.00",
            "location": random.choice(Warehouse.objects.all()).pk,
            "assigned_user": random.choice(User.objects.all()).pk,
            "status": "Updated Status",
            "distributor": "Updated Distributor",
            "warranty_service_info": "Updated Warranty",
            "notes": "Updated Notes",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_device(self):
        device = Device.objects.first()
        self.assertIsNotNone(device, "No device found in the database.")
        url = reverse("device-detail", kwargs={"pk": device.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_warehouse(self):
        warehouse = Warehouse.objects.first()
        self.assertIsNotNone(warehouse, "No warehouse found in the database.")
        url = reverse("warehouse-detail", kwargs={"pk": warehouse.pk})
        data = {
            "warehouse_number": 11,
            "name": "Updated Warehouse Name",
            "country": "Updated Country",
            "city": "Updated City",
            "postal_code": "54321",
            "phone": "9876543210",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_warehouse(self):
        warehouse = Warehouse.objects.first()
        self.assertIsNotNone(warehouse, "No warehouse found in the database.")
        url = reverse("warehouse-detail", kwargs={"pk": warehouse.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_donor(self):
        donor = Donor.objects.first()
        self.assertIsNotNone(donor, "No donor found in the database.")
        url = reverse("donor-detail", kwargs={"pk": donor.pk})
        data = {
            "name": "Updated Donor Name",
            "contact_info": "Updated Contact Info",
            "address": "Updated Address",
            "email": "updateddonor@example.com",
            "phone": "8765432109",
        }
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_donor(self):
        donor = Donor.objects.first()
        self.assertIsNotNone(donor, "No donor found in the database.")
        url = reverse("donor-detail", kwargs={"pk": donor.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
