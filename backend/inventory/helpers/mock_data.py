import random
from datetime import timedelta

from django.db.models import Max
from django.utils import timezone

from ..models import Device, Donor, Location, Shipping, User


def generate_mock_location(num_locations):
    locations = []
    # Get the maximum existing location number
    max_location_number = (
        Location.objects.aggregate(Max("location_id"))["location_id__max"] or 0
    )

    for i in range(num_locations):
        location = {
            "name": f"Location {max_location_number + i + 1}",
            "type": random.choice(
                ["Warehouse", "Distribution Center", "Repair Center"]
            ),
            "address": f"Address {max_location_number + i + 1}, Street {random.randint(1, 100)}",
            "country": random.choice(["USA", "Canada", "UK", "Germany", "France"]),
            "city": f"City {max_location_number + i + 1}",
            "postal_code": f"{random.randint(10000, 99999)}",
            "phone": f"+1-{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
        }
        locations.append(location)
    return locations


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


def generate_mock_shipping(num_shipping, locations):
    shippings = []
    for _ in range(num_shipping):
        shipping = {
            "destination": random.choice(locations),
            "arrived": random.choice([True, False]),
            "date_shipped": (
                timezone.now() - timedelta(days=random.randint(1, 30))
            ).date(),
            "date_delivered": (
                (timezone.now() - timedelta(days=random.randint(0, 29))).date()
                if random.choice([True, False])
                else None
            ),
            "tracking_identifier": f"TRACK-{random.randint(100000, 999999)}",
        }
        shippings.append(shipping)
    return shippings


def generate_mock_device(num_devices, locations, donors, users, shippings):
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
            "date_received": (
                timezone.now() - timedelta(days=random.randint(1, 30))
            ).date(),
            "created_by": random.choice(users) if users else None,
            "received_by": random.choice(users) if users else None,
            "physical_condition": random.choice(["Excellent", "Good", "Fair", "Poor"]),
            "specifications": f"Specs for Device {existing_devices_count + i + 1}",
            "operating_system": random.choice(
                ["Windows 10", "macOS", "Linux", "Android", "iOS"]
            ),
            "donor": random.choice(donors) if donors else None,
            "date_of_donation": (
                timezone.now() - timedelta(days=random.randint(1, 180))
            ).date(),
            "value": round(random.uniform(100, 1000), 2),
            "start_location": random.choice(locations) if locations else None,
            "end_location": random.choice(locations) if locations else None,
            "notes": f"Notes for Device {existing_devices_count + i + 1}",
        }
        devices.append(device)
    return devices


def create_mock_data(num_locations=5, num_donors=10, num_devices=50, num_shipping=20):
    # Generate mock data
    new_locations = generate_mock_location(num_locations)
    new_donors = generate_mock_donor(num_donors)

    # Create location and donor objects
    created_locations = Location.objects.bulk_create(
        [Location(**l) for l in new_locations]
    )
    created_donors = Donor.objects.bulk_create([Donor(**d) for d in new_donors])

    # Get all locations, donors, and users for device and shipping creation
    all_locations = list(Location.objects.all())
    all_donors = list(Donor.objects.all())
    all_users = list(User.objects.all())

    # Generate and create shipping objects
    new_shippings = generate_mock_shipping(num_shipping, all_locations)
    created_shippings = Shipping.objects.bulk_create(
        [Shipping(**s) for s in new_shippings]
    )

    # Generate and create device objects
    new_devices = generate_mock_device(
        num_devices, all_locations, all_donors, all_users, created_shippings
    )
    created_devices = Device.objects.bulk_create([Device(**d) for d in new_devices])

    # Add shipping information to devices
    for device in created_devices:
        device.shipping_infos.set(
            random.sample(created_shippings, random.randint(0, 3))
        )

    return {
        "locations_created": len(created_locations),
        "donors_created": len(created_donors),
        "shippings_created": len(created_shippings),
        "devices_created": len(created_devices),
    }
