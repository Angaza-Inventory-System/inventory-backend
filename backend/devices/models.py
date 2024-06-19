import uuid
from django.db import models
from backend.users.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator

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


    warehouse_number = models.IntegerField(
        primary_key=True,
        help_text="Physical identifier for the warehouse, not randomly generated."
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the warehouse."
    )
    country = models.CharField(
        max_length=100,
        help_text="Country where the warehouse is located."
    )
    city = models.CharField(
        max_length=100,
        help_text="City where the warehouse is located."
    )
    postal_code = models.CharField(
        max_length=20,
        help_text="Postal code of the warehouse's location."
    )
    phone = models.CharField(
        max_length=20,
        help_text="Phone number of the warehouse."
    )


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

    donor_id = models.AutoField(
        primary_key=True,
        help_text="Unique identifier for the donor."
    )
    name = models.CharField(
        max_length=255,
        help_text="Name of the donor."
    )
    contact_info = models.CharField(
        max_length=255,
        help_text="Contact information of the donor."
    )
    address = models.TextField(
        help_text="Address of the donor."
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
        help_text="Email address of the donor."
    )
    phone = models.CharField(
        max_length=20,
        help_text="Phone number of the donor."
    )

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
                - No specific constraints mentioned.
        shipment_date (DateField): The date when the device was shipped.
            - Constraints:
                - No specific constraints mentioned.
        date_received (DateField): The date when the device was received.
            - Constraints:
                - No specific constraints mentioned.
        received_by (ForeignKey): The user who received the device.
            - Constraints:
                - Must be a foreign key to the User model (ForeignKey).
        physical_condition (CharField): The physical condition of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        specifications (TextField): The specifications of the device.
            - Constraints:
                - No specific constraints mentioned.
        operating_system (CharField): The operating system of the device.
            - Constraints:
                - Must be between 1 and 100 characters in length.
        accessories (TextField): The accessories of the device.
            - Constraints:
                - No specific constraints mentioned.
        donor (ForeignKey): The donor of the device.
            - Constraints:
                - Must be a foreign key to the Donor model (ForeignKey).
        date_of_donation (DateField): The date when the device was donated.
            - Constraints:
                - No specific constraints mentioned.
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
                - No specific constraints mentioned.
        notes (TextField): Additional notes about the device.
            - Constraints:
                - No specific constraints mentioned.
    """
      device_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        help_text="Unique identifier for the device."
    )
      type = models.CharField(
        max_length=100,
        help_text="Type of the device."
    )
      make = models.CharField(
        max_length=100,
        help_text="Make of the device."
    )
      model = models.CharField(
        max_length=100,
        help_text="Model of the device."
    )
      serial_number = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="Serial number of the device (unique identifier)."
    )
      mac_id = models.CharField(
        max_length=100,
        unique=True,
        db_index=True,
        help_text="MAC ID of the device (unique identifier)."
    )
      year_of_manufacture = models.IntegerField(
        help_text="Year of manufacture of the device."
    )
      shipment_date = models.DateField(
        help_text="Date when the device was shipped."
    )
      date_received = models.DateField(
        help_text="Date when the device was received."
    )
      received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="received_devices",
        help_text="User who received the device."
    )
      physical_condition = models.CharField(
        max_length=100,
        help_text="Physical condition of the device."
    )
      specifications = models.TextField(
        help_text="Specifications of the device."
    )
      operating_system = models.CharField(
        max_length=100,
        help_text="Operating system of the device."
    )
      accessories = models.TextField(
        help_text="Accessories of the device."
    )
      donor = models.ForeignKey(
        Donor,
        on_delete=models.CASCADE,
        help_text="Donor of the device."
    )
      date_of_donation = models.DateField(
        help_text="Date when the device was donated."
    )
      value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Value of the device, provided by accounting."
    )
      location = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        help_text="Location of the device in the warehouse."
    )
      assigned_user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="assigned_devices",
        help_text="User to whom the device is assigned."
    )
      status = models.CharField(
        max_length=100,
        help_text="Status of the device."
    )
      distributor = models.CharField(
        max_length=100,
        help_text="Distributor of the device."
    )
      warranty_service_info = models.TextField(
        help_text="Warranty and service information of the device."
    )
      notes = models.TextField(
        help_text="Additional notes about the device."
    )
