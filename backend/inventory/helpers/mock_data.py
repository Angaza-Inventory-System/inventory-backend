import random
from datetime import timedelta

from django.db.models import Max
from django.utils import timezone

from ..models import Device, Donor, Location


def generate_mock_warehouse(num_warehouses):
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
