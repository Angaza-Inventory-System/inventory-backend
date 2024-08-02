import random
from datetime import timedelta

from django.db.models import Max
from django.utils import timezone

from ..models import Device, Donor, Location

def generate_mock_warehouse(num_warehouses):
    """
    Generates a list of mock warehouse data.

    Args:
        num_warehouses (int): The number of mock warehouses to generate.

    Returns:
        list: A list of dictionaries, each representing a mock warehouse.
              Each dictionary contains the following keys:
              - "warehouse_number": The physical identifier for the warehouse.
              - "name": The name of the warehouse.
              - "country": The country where the warehouse is located.
              - "city": The city where the warehouse is located.
              - "postal_code": The postal code of the warehouse's location.
              - "phone": The phone number of the warehouse.
    """
    warehouses = []
    # Get the maximum existing warehouse number
    max_warehouse_number = (
        Location.objects.aggregate(Max("warehouse_number"))["warehouse_number__max"]
        or 0
    )

    for i in range(num_warehouses):
        warehouse = {
            "warehouse_number": max_warehouse_number + i + 1,
            "name": f"Warehouse {max_warehouse_number + i + 1}",
            "country": random.choice(["USA", "Canada", "UK", "Germany", "France"]),
            "city": f"City {max_warehouse_number + i + 1}",
            "postal_code": f"{random.randint(10000, 99999)}",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        }
        warehouses.append(warehouse)
    return warehouses


def generate_mock_donor(num_donors):
    """
    Generates a list of mock donor data.

    Args:
        num_donors (int): The number of mock donors to generate.

    Returns:
        list: A list of dictionaries, each representing a mock donor.
              Each dictionary contains the following keys:
              - "name": The name of the donor.
              - "contact_info": The contact information of the donor.
              - "address": The address of the donor.
              - "email": The email address of the donor.
              - "phone": The phone number of the donor.
    """
    donors = []
    # Get the count of existing donors
    existing_donors_count = Donor.objects.count()

    for i in range(num_donors):
        donor = {
            "name": f"Donor {existing_donors_count + i + 1}",
            "contact_info": f"Contact {existing_donors_count + i + 1}",
            "address": f"Address {existing_donors_count + i + 1}, City {existing_donors_count + i + 1}",
            "email": f"donor{existing_donors_count + i + 1}@example.com",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        }
        donors.append(donor)
    return donors


def generate_mock_device(num_devices, warehouses, donors, users):
    """
    Generates a list of mock device data.

    Args:
        num_devices (int): The number of mock devices to generate.
        warehouses (list): A list of mock warehouse dictionaries to assign locations.
        donors (list): A list of mock donor dictionaries to assign donors.
        users (list): A list of users to assign as `received_by` and `created_by`.

    Returns:
        list: A list of dictionaries, each representing a mock device.
              Each dictionary contains the following keys:
              - "type": The type of the device.
              - "make": The make of the device.
              - "model": The model of the device.
              - "serial_number": The serial number of the device.
              - "mac_id": The MAC ID of the device.
              - "year_of_manufacture": The year the device was manufactured.
              - "shipment_date": The date the device was shipped.
              - "date_received": The date the device was received.
              - "received_by": The user who received the device.
              - "physical_condition": The physical condition of the device.
              - "specifications": The specifications of the device.
              - "operating_system": The operating system of the device.
              - "accessories": The accessories included with the device.
              - "donor": The donor of the device.
              - "date_of_donation": The date the device was donated.
              - "value": The value of the device.
              - "location": The location (warehouse) where the device is stored.
              - "created_by": The user who created the device record.
              - "status": The status of the device.
              - "distributor": The distributor of the device.
              - "warranty_service_info": The warranty service information for the device.
              - "notes": Additional notes about the device.
    """
    devices = []
    # Get the count of existing devices
    existing_devices_count = Device.objects.count()

    for i in range(num_devices):
        device = {
            "type": random.choice(["Laptop", "Desktop", "Tablet", "Smartphone"]),
            "make": random.choice(["Dell", "HP", "Lenovo", "Apple", "Samsung"]),
            "model": f"Model {existing_devices_count + i + 1}",
            "serial_number": f"SN-{existing_devices_count + i + 1}-{random.randint(10000, 99999)}",
            "mac_id": f"MAC-{existing_devices_count + i + 1}-{random.randint(100000, 999999)}",
            "year_of_manufacture": random.randint(2015, 2023),
            "shipment_date": (
                timezone.now() - timedelta(days=random.randint(1, 365))
            ).date(),
            "date_received": (
                timezone.now() - timedelta(days=random.randint(1, 30))
            ).date(),
            "received_by": random.choice(users) if users else None,
            "physical_condition": random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "specifications": f"Specs for Device {existing_devices_count + i + 1}",
            "operating_system": random.choice(
                ["Windows 10", "macOS", "Linux", "Android", "iOS"]
            ),
            "accessories": f"Accessories for Device {existing_devices_count + i + 1}",
            "donor": random.choice(donors) if donors else None,
            "date_of_donation": (
                timezone.now() - timedelta(days=random.randint(1, 180))
            ).date(),
            "value": round(random.uniform(100, 1000), 2),
            "location": random.choice(warehouses) if warehouses else None,
            "created_by": random.choice(users) if users else None,
            "status": random.choice(["Available", "In Use", "Under Repair", "Retired"]),
            "distributor": f"Distributor {existing_devices_count + i + 1}",
            "warranty_service_info": f"Warranty info for Device {existing_devices_count + i + 1}",
            "notes": f"Notes for Device {existing_devices_count + i + 1}",
        }
        devices.append(device)
    return devices
