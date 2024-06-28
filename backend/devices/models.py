import uuid

from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.users.models import User


class Warehouse(models.Model):
    """
    Represents a warehouse in the inventory system.

    Attributes:
        warehouse_number (int): The physical identifier for the warehouse, not
            randomly generated.
            - Constraints:
                - Must be an integer (primary key).
        name (str): The name of the warehouse.
            - Constraints:
                - Must be between 1 and 255 characters in length.
        country (str): The country where the warehouse is located.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        city (str): The city where the warehouse is located.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        postal_code (str): The postal code of the warehouse's location.
            - Constraints:
                - Must be between 1 and 20 characters in length.
        phone (str): The phone number of the warehouse.
            - Constraints:
                - Must be between 1 and 20 characters in length.
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
        accessories (TextField): The accessories of the device.
            - Constraints:
                - No specific constraints.
        donor (ForeignKey): The donor of the device.
            - Constraints:
                - Must be a foreign key to the Donor model (ForeignKey).
        date_of_donation (DateField): The date when the device was donated.
            - Constraints:
                - No specific constraints.
        value (DecimalField): The value of the device, provided by accounting.
            - Constraints:
                - Must be a decimal number with up to 10 digits and 2 decimal places (DecimalField).
        location (ForeignKey): The location of the device in the warehouse.
            - Constraints:
                - Must be a foreign key to the Warehouse model (ForeignKey).
        assigned_user (ForeignKey): The user to whom the device is assigned.
            - Constraints:
                - Must be a foreign key to the User model (ForeignKey).
        status (CharField): The status of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
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
        help_text="MAC ID of the device (unique identifier).",
    )
    year_of_manufacture = models.IntegerField()
    shipment_date = models.DateField()
    date_received = models.DateField()
    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_devices",
    )
    physical_condition = models.CharField(max_length=100)
    specifications = models.TextField()
    operating_system = models.CharField(max_length=100)
    accessories = models.TextField()
    donor = models.ForeignKey(
        Donor, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name="donated_devices", 
    )
    date_of_donation = models.DateField()
    value = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        related_name="stored_items"
    )
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_devices",
    )
    status = models.CharField(max_length=100)
    distributor = models.CharField(max_length=100)
    warranty_service_info = models.TextField()
    notes = models.TextField()
