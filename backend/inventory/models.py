import uuid

from django.core.validators import EmailValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from backend.users.models import User


class Shipment(models.Model):
    """
    Represents a shipment in the inventory system.

    Attributes:
        shipping_id (int): The unique identifier for the shipment.
            - Constraints:
                - Automatically generated (AutoField).
        destination (ForeignKey): The location to which the shipment is sent.
            - Constraints:
                - Must be a foreign key to the Location model.
                - Can be null (on_delete=models.SET_NULL).
        arrived (bool): Indicates whether the shipment has arrived.
            - Constraints:
                - Defaults to False.
        date_shipped (date): The date when the shipment was dispatched.
            - Constraints:
                - No specific constraints.
        date_delivered (date): The date when the shipment was delivered.
            - Constraints:
                - Can be null.
        tracking_identifier (str): The tracking number for the shipment.
            - Constraints:
                - Maximum length of 100 characters.
                - Can be blank.
    """
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
    Represents a location (e.g., warehouse) in the inventory system.

    Attributes:
        location_id (int): The unique identifier for the location.
            - Constraints:
                - Automatically generated (AutoField).
        name (str): The name of the location.
            - Constraints:
                - Must be between 1 and 255 characters in length.
        type (str): The type of the location.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        address (str): The address of the location.
            - Constraints:
                - Maximum length of 500 characters.
                - Must be unique.
        country (str): The country where the location is situated.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        city (str): The city where the location is situated.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        postal_code (str): The postal code of the location.
            - Constraints:
                - Must be between 1 and 20 characters in length.
        phone (str): The phone number of the location.
            - Constraints:
                - Maximum length of 20 characters.
                - Can be blank.
                - Must be unique.
    """
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    address = models.TextField(max_length=500, unique=True)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20, blank=True, unique=True)


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
                - No specific constraints.
        email (str): The email address of the donor.
            - Constraints:
                - Must be a valid email format.
                - Must be unique (EmailField).
                - Indexed in the database (db_index=True).
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
        device_id (UUID): The unique identifier for the device.
            - Constraints:
                - Automatically generated (UUIDField).
        type (str): The type of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        make (str): The make of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        model (str): The model of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        serial_number (str): The serial number of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
                - Must be unique (CharField with unique=True).
        mac_id (str): The MAC ID of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
                - Must be unique (CharField with unique=True).
                - Can be blank.
        year_of_manufacture (int): The year when the device was manufactured.
            - Constraints:
                - No specific constraints.
        date_received (date): The date when the device was received.
            - Constraints:
                - No specific constraints.
        created_by (ForeignKey): The user who created the device record.
            - Constraints:
                - Must be a foreign key to the User model.
                - Can be null (on_delete=models.SET_NULL).
        received_by (ForeignKey): The user who received the device.
            - Constraints:
                - Must be a foreign key to the User model.
                - Can be null (on_delete=models.SET_NULL).
        physical_condition (str): The physical condition of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        specifications (str): The specifications of the device.
            - Constraints:
                - Can be blank.
        operating_system (str): The operating system of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        donor (ForeignKey): The donor of the device.
            - Constraints:
                - Must be a foreign key to the Donor model.
                - Can be null (on_delete=models.SET_NULL).
        date_of_donation (date): The date when the device was donated.
            - Constraints:
                - No specific constraints.
        value (Decimal): The monetary value of the device.
            - Constraints:
                - Must be a decimal number with up to 10 digits and 2 decimal places (DecimalField).
        start_location (ForeignKey): The initial location of the device.
            - Constraints:
                - Must be a foreign key to the Location model.
                - Can be null (on_delete=models.SET_NULL).
        end_location (ForeignKey): The current location of the device.
            - Constraints:
                - Must be a foreign key to the Location model.
                - Can be null (on_delete=models.SET_NULL).
        notes (str): Additional notes about the device.
            - Constraints:
                - Can be blank.
        shipping_infos (ManyToManyField): The shipments associated with the device.
            - Constraints:
                - Can be blank.
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
