import uuid

from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.users.models import User


class Shipment(models.Model):
    shipping_id = models.AutoField(primary_key=True)
    destination = models.ForeignKey(
        "Location",
        on_delete=models.SET_NULL,
        null=True,
        related_name="destination_shipments",
    )
    arrived = models.BooleanField(default=False)
    date_shipped = models.DateField()
    date_delivered = models.DateField(null=True)
    tracking_identifier = models.CharField(max_length=100, blank=True)


class Location(models.Model):
    """
    Represents a warehouse in the inventory system.

    Attributes:
        warehouse_number (int): The physical identifier for the warehouse, automatically generated.
        - Constraints:
            - Automatically generated (AutoField).
        name (str): The name of the warehouse.
            - Constraints:
                - Must be between 1 and 255 characters in length.
        type (str): The type of the warehouse.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        address (str): The address of the warehouse.
            - Constraints:
                - No specific constraints
        country (str): The country where the warehouse is located.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        city (str): The city where the warehouse is located.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        postal_code (str): The postal code of the warehouse.
            - Constraints:
                - Must be between 1 and 20 characters in length.
        phone (str): The phone number of the warehouse.
            - Constraints:
                - Must be between 1 and 20 characters in
    """

    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    address = models.TextField(max_length=500, unique=True,)
    country = models.CharField(max_length=100, )
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, unique=True,)


class Donor(models.Model):
    """
    Represents a donor in the inventory system.

    Attributes:
        donor_id (int): The unique identifier for the donor.
            - Constraints:
                - Automatically generated (AutoField).
        name (str): The name of the donor.
            - Constraints:
                - Must be between 1 and 255 characters in length.
        contact_info (str): The contact information of the donor.
            - Constraints:
                - Must be between 1 and 255 characters in length.
        address (str): The address of the donor.
            - Constraints:
                - No specific constraints
        email (str): The email address of the donor.
            - Constraints:
                - Must be a valid email format.
                - Must be unique across donors (EmailField).
        phone (str): The phone number of the donor.
            - Constraints:
                - Must be between 1 and 20 characters in length.
    """

    donor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    address = models.TextField()
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
    )
    phone = models.CharField(max_length=20)


class Device(models.Model):
    """
    Represents a device in the inventory system.

    Attributes:
        device_id (UUIDField): The unique identifier for the device.
            - Constraints:
                - Automatically generated (UUIDField).
        type (CharField): The type of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        make (CharField): The make of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        model (CharField): The model of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        serial_number (CharField): The serial number of the device (unique).
            - Constraints:
                - Must be between 1 and 100 characters in length.
                - Must be unique (CharField with unique=True).
        mac_id (CharField): The MAC ID of the device (unique).
            - Constraints:
                - Must be between 1 and 100 characters in length.
                - Must be unique (CharField with unique=True).
        year_of_manufacture (IntegerField): The year of manufacture of the device.
            - Constraints:
                - No specific constraints.
        shipment_date (DateField): The date when the device was shipped.
            - Constraints:
                - No specific constraints.
        date_received (DateField): The date when the device was received.
            - Constraints:
                - No specific constraints.
        received_by (ForeignKey): The user who received the device.
            - Constraints:
                - Must be a foreign key to the User model (ForeignKey).
        physical_condition (CharField): The physical condition of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        specifications (TextField): The specifications of the device.
            - Constraints:
                - No specific constraints.
        operating_system (CharField): The operating system of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        donor (ForeignKey): The donor of the device.
            - Constraints:
                - Must be a foreign key to the Donor model (ForeignKey).
        date_of_donation (DateField): The date when the device was donated.
            - Constraints:
                - No specific constraints.
        value (DecimalField): The value of the device, provided by accounting.
            - Constraints:a
                - Must be a decimal number with up to 10 digits and 2 decimal places (DecimalField).
        location (ForeignKey): The location of the device in the warehouse.
            - Constraints:
                - Must be a foreign key to the Warehouse model (ForeignKey).
        created_by (ForeignKey): The user to whom the device is assigned.
            - Constraints:
                - Must be a foreign key to the User model (ForeignKey).
        distributor (CharField): The distributor of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        warranty_service_info (TextField): The warranty and service information
            of the device.
            - Constraints:
                - No specific constraints.
        notes (TextField): Additional notes about the device.
            - Constraints:
                - No specific constraints.
    """

    device_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    type = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    serial_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
    )
    mac_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        blank=True,
    )
    year_of_manufacture = models.IntegerField()
    date_received = models.DateField()
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_devices",
    )
    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_devices",
    )
    physical_condition = models.CharField(max_length=100)
    specifications = models.TextField(blank=True)
    operating_system = models.CharField(max_length=100)
    donor = models.ForeignKey(
        Donor,
        on_delete=models.SET_NULL,
        null=True,
        related_name="donated_devices",
    )
    date_of_donation = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    start_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="stored_items"
    )
    end_location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, related_name="received_items"
    )
    notes = models.TextField(blank=True)
    shipping_infos = models.ManyToManyField(
        Shipment, related_name="devices", blank=True
    )
