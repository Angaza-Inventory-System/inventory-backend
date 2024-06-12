import uuid

from django.db import models

from backend.auth.models import User


class Warehouse(models.Model):
    warehouse_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)


class Donor(models.Model):
    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)


class Device(models.Model):
    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    mac_id = models.CharField(max_length=100, unique=True)
    year_of_manufacture = models.IntegerField()
    shipment_date = models.DateField()
    date_received = models.DateField()
    received_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="received_devices"
    )
    physical_condition = models.CharField(max_length=100)
    specifications = models.TextField()
    operating_system = models.CharField(max_length=100)
    accessories = models.TextField()
    donor = models.ForeignKey(Donor, on_delete=models.CASCADE)
    date_of_donation = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(Warehouse, on_delete=models.SET_NULL, null=True)
    assigned_user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="assigned_devices"
    )
    status = models.CharField(max_length=100)
    distributor = models.CharField(max_length=100)
    warranty_service_info = models.TextField()
    notes = models.TextField()
