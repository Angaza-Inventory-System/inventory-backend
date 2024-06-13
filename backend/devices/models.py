import uuid

from django.db import models

from backend.auth.models import User


class Warehouse(models.Model):
    """
    Represents a warehouse in the inventory system.

    Attributes:
        warehouse_number (int): The physical identifier for the warehouse, not
        randomly generated.
        name (str): The name of the warehouse.
        country (str): The country where the warehouse is located.
        city (str): The city where the warehouse is located.
        postal_code (str): The postal code of the warehouse's location.
        phone (str): The phone number of the warehouse.
    """

    warehouse_number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)


class Donor(models.Model):
    """
    Represents a donor in the inventory system.

    Attributes:
        donor_id (int): The unique identifier for the donor.
        name (str): The name of the donor.
        contact_info (str): The contact information of the donor.
        address (str): The address of the donor.
        email (str): The email address of the donor.
        phone (str): The phone number of the donor.
    """

    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=20)


class Device(models.Model):
    """
    Represents a device in the inventory system.

    Attributes:
        device_id (UUIDField): The unique identifier for the device.
        type (CharField): The type of the device.
        make (CharField): The make of the device.
        model (CharField): The model of the device.
        serial_number (CharField): The serial number of the device (unique).
        mac_id (CharField): The MAC ID of the device (unique).
        year_of_manufacture (IntegerField): The year of manufacture of the device.
        shipment_date (DateField): The date when the device was shipped.
        date_received (DateField): The date when the device was received.
        received_by (ForeignKey): The user who received the device.
        physical_condition (CharField): The physical condition of the device.
        specifications (TextField): The specifications of the device.
        operating_system (CharField): The operating system of the device.
        accessories (TextField): The accessories of the device.
        donor (ForeignKey): The donor of the device.
        date_of_donation (DateField): The date when the device was donated.
        value (DecimalField): The value of the device, provided by accounting.
        location (ForeignKey): The location of the device in the warehouse.
        assigned_user (ForeignKey): The user to whom the device is assigned.
        status (CharField): The status of the device.
        distributor (CharField): The distributor of the device.
        warranty_service_info (TextField): The warranty and service information
        of the device.
        notes (TextField): Additional notes about the device.
    """

    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True, db_index=True)
    mac_id = models.CharField(max_length=100, unique=True, db_index=True)
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