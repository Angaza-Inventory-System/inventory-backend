import logging

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from backend.inventory.models import Device, Donor, Warehouse
from backend.users.models import User

# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class DeviceSearchTestCase(TestCase):
    def setUp(self):
        # Create API client
        self.client = APIClient()

        # Register users via endpoint
        user1_response = self.client.post(
            "/users/register/",
            {
                "username": "user1",
                "email": "user1@example.com",
                "password": "P@ssword123",
                "role": "admin",
                "first_name": "First1",
                "last_name": "Last1",
            },
            format="json",
        )
        self.assertEqual(user1_response.status_code, status.HTTP_201_CREATED)

        user2_response = self.client.post(
            "/users/register/",
            {
                "username": "user2",
                "email": "user2@example.com",
                "password": "P@ssword123",
                "role": "user",
                "first_name": "First2",
                "last_name": "Last2",
            },
            format="json",
        )
        self.assertEqual(user2_response.status_code, status.HTTP_201_CREATED)

        # Authenticate and get tokens
        login_response = self.client.post(
            "/authen/login/",
            {"username": "user1", "password": "P@ssword123"},
            format="json",
        )
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)
        self.access_token = login_response.json()["tokens"]["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token)

        # Create warehouses via endpoint
        warehouse1_response = self.client.post(
            "/devices/warehouses/",
            {
                "warehouse_number": 1,
                "name": "Warehouse1",
                "country": "Country1",
                "city": "City1",
                "postal_code": "12345",
                "phone": "1234567890",
            },
            format="json",
        )
        self.assertEqual(warehouse1_response.status_code, status.HTTP_201_CREATED)

        warehouse2_response = self.client.post(
            "/devices/warehouses/",
            {
                "warehouse_number": 2,
                "name": "Warehouse2",
                "country": "Country2",
                "city": "City2",
                "postal_code": "67890",
                "phone": "0987654321",
            },
            format="json",
        )
        self.assertEqual(warehouse2_response.status_code, status.HTTP_201_CREATED)

        # Create donors via endpoint
        donor1_response = self.client.post(
            "/devices/donors/",
            {
                "name": "Donor1",
                "contact_info": "Contact1",
                "address": "Address1",
                "email": "donor1@example.com",
                "phone": "1112223333",
            },
            format="json",
        )
        self.assertEqual(donor1_response.status_code, status.HTTP_201_CREATED)

        donor2_response = self.client.post(
            "/devices/donors/",
            {
                "name": "Donor2",
                "contact_info": "Contact2",
                "address": "Address2",
                "email": "donor2@example.com",
                "phone": "4445556666",
            },
            format="json",
        )
        self.assertEqual(donor2_response.status_code, status.HTTP_201_CREATED)

        # Create devices via endpoint
        device_data = [
            {
                "device_id": "1a2b3c4d-1234-5678-1234-567812345681",
                "type": "Laptop",
                "make": "MakeD",
                "model": "ModelD",
                "serial_number": "SN004",
                "mac_id": "MAC004",
                "year_of_manufacture": 2019,
                "shipment_date": "2019-04-01",
                "date_received": "2019-04-02",
                "received_by": 2,
                "physical_condition": "Good",
                "specifications": "SpecsD",
                "operating_system": "OS_D",
                "accessories": "AccD",
                "donor": 2,
                "date_of_donation": "2019-04-01",
                "value": 400.00,
                "location": 2,
                "created_by": 1,
                "status": "Available",
                "distributor": "DistD",
                "warranty_service_info": "WarrantyD",
                "notes": "NotesD",
            },
            {
                "device_id": "1a2b3c4d-1234-5678-1234-567812345682",
                "type": "Desktop",
                "make": "MakeE",
                "model": "ModelE",
                "serial_number": "SN005",
                "mac_id": "MAC005",
                "year_of_manufacture": 2018,
                "shipment_date": "2018-05-01",
                "date_received": "2018-05-02",
                "received_by": 1,
                "physical_condition": "Fair",
                "specifications": "SpecsE",
                "operating_system": "OS_E",
                "accessories": "AccE",
                "donor": 1,
                "date_of_donation": "2018-05-01",
                "value": 500.00,
                "location": 1,
                "created_by": 2,
                "status": "In Repair",
                "distributor": "DistE",
                "warranty_service_info": "WarrantyE",
                "notes": "NotesE",
            },
            {
                "device_id": "1a2b3c4d-1234-5678-1234-567812345683",
                "type": "Laptop",
                "make": "MakeF",
                "model": "ModelF",
                "serial_number": "SN006",
                "mac_id": "MAC006",
                "year_of_manufacture": 2017,
                "shipment_date": "2017-06-01",
                "date_received": "2017-06-02",
                "received_by": 2,
                "physical_condition": "Excellent",
                "specifications": "SpecsF",
                "operating_system": "OS_F",
                "accessories": "AccF",
                "donor": 2,
                "date_of_donation": "2017-06-01",
                "value": 600.00,
                "location": 2,
                "created_by": 1,
                "status": "Available",
                "distributor": "DistF",
                "warranty_service_info": "WarrantyF",
                "notes": "NotesF",
            },
            {
                "device_id": "1a2b3c4d-1234-5678-1234-567812345684",
                "type": "Desktop",
                "make": "MakeG",
                "model": "ModelG",
                "serial_number": "SN007",
                "mac_id": "MAC007",
                "year_of_manufacture": 2016,
                "shipment_date": "2016-07-01",
                "date_received": "2016-07-02",
                "received_by": 1,
                "physical_condition": "Good",
                "specifications": "SpecsG",
                "operating_system": "OS_G",
                "accessories": "AccG",
                "donor": 1,
                "date_of_donation": "2016-07-01",
                "value": 700.00,
                "location": 1,
                "created_by": 2,
                "status": "In Repair",
                "distributor": "DistG",
                "warranty_service_info": "WarrantyG",
                "notes": "NotesG",
            },
            {
                "device_id": "1a2b3c4d-1234-5678-1234-567812345685",
                "type": "Laptop",
                "make": "MakeH",
                "model": "ModelH",
                "serial_number": "SN008",
                "mac_id": "MAC008",
                "year_of_manufacture": 2022,
                "shipment_date": "2015-08-01",
                "date_received": "2015-08-02",
                "received_by": 2,
                "physical_condition": "Fair",
                "specifications": "SpecsH",
                "operating_system": "OS_H",
                "accessories": "AccH",
                "donor": 2,
                "date_of_donation": "2015-08-01",
                "value": 800.00,
                "location": 2,
                "created_by": 1,
                "status": "Available",
                "distributor": "DistH",
                "warranty_service_info": "WarrantyH",
                "notes": "NotesH",
            },
            {
                "device_id": "1a2b3c4d-1234-5678-1234-567812345686",
                "type": "Desktop",
                "make": "MakeI",
                "model": "ModelI",
                "serial_number": "SN009",
                "mac_id": "MAC009",
                "year_of_manufacture": 2014,
                "shipment_date": "2014-09-01",
                "date_received": "2014-09-02",
                "received_by": 1,
                "physical_condition": "Excellent",
                "specifications": "SpecsI",
                "operating_system": "OS_I",
                "accessories": "AccI",
                "donor": 1,
                "date_of_donation": "2014-09-01",
                "value": 900.00,
                "location": 1,
                "created_by": 2,
                "status": "Available",
                "distributor": "DistI",
                "warranty_service_info": "WarrantyI",
                "notes": "NotesI",
            },
        ]

        for device in device_data:
            response = self.client.post("/devices/devices/", device, format="json")
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_search_by_device_id(self):
        response = self.client.get(
            "/devices/devices/", {"search": "1a2b3c4d-1234-5678-1234-567812345681"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 1)
        self.assertEqual(
            results[0]["device_id"], "1a2b3c4d-1234-5678-1234-567812345681"
        )

    def test_fuzzy_search_by_device_id(self):
        response = self.client.get(
            "/devices/devices/", {"search": "1a2b3c4d-1234-5678-1234-56781234568"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_type(self):
        response = self.client.get("/devices/devices/", {"search": "Laptop"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["type"] == "Laptop" for result in results))

    def test_fuzzy_search_by_type(self):
        response = self.client.get("/devices/devices/", {"search": "Lapto"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_make(self):
        response = self.client.get("/devices/devices/", {"search": "MakeD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["make"] == "MakeD" for result in results))

    def test_fuzzy_search_by_make(self):
        response = self.client.get("/devices/devices/", {"search": "MakD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_model(self):
        response = self.client.get("/devices/devices/", {"search": "ModelD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["model"] == "ModelD" for result in results))

    def test_fuzzy_search_by_model(self):
        response = self.client.get("/devices/devices/", {"search": "MdelD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_serial_number(self):
        response = self.client.get("/devices/devices/", {"search": "SN004"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["serial_number"] == "SN004" for result in results))

    def test_fuzzy_search_by_serial_number(self):
        response = self.client.get("/devices/devices/", {"search": "SN00"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_mac_id(self):
        response = self.client.get("/devices/devices/", {"search": "MAC004"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["mac_id"] == "MAC004" for result in results))

    def test_fuzzy_search_by_mac_id(self):
        response = self.client.get("/devices/devices/", {"search": "MAC00"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_year_of_manufacture(self):
        response = self.client.get("/devices/devices/", {"search": "2019"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["year_of_manufacture"] == 2019 for result in results)
        )

    def test_fuzzy_search_by_year_of_manufacture(self):
        response = self.client.get("/devices/devices/", {"search": "201"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_shipment_date(self):
        response = self.client.get("/devices/devices/", {"search": "2019-04-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["shipment_date"] == "2019-04-01" for result in results)
        )

    def test_fuzzy_search_by_shipment_date(self):
        response = self.client.get("/devices/devices/", {"search": "2019-04"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_date_received(self):
        response = self.client.get("/devices/devices/", {"search": "2019-04-02"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["date_received"] == "2019-04-02" for result in results)
        )

    def test_fuzzy_search_by_date_received(self):
        response = self.client.get("/devices/devices/", {"search": "2019-04"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_physical_condition(self):
        response = self.client.get("/devices/devices/", {"search": "Good"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["physical_condition"] == "Good" for result in results)
        )

    def test_fuzzy_search_by_physical_condition(self):
        response = self.client.get("/devices/devices/", {"search": "Goo"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_specifications(self):
        response = self.client.get("/devices/devices/", {"search": "SpecsD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["specifications"] == "SpecsD" for result in results))

    def test_fuzzy_search_by_specifications(self):
        response = self.client.get("/devices/devices/", {"search": "SpecsD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_operating_system(self):
        response = self.client.get("/devices/devices/", {"search": "OS_D"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["operating_system"] == "OS_D" for result in results))

    def test_fuzzy_search_by_operating_system(self):
        response = self.client.get("/devices/devices/", {"search": "OS_D"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_accessories(self):
        response = self.client.get("/devices/devices/", {"search": "AccD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["accessories"] == "AccD" for result in results))

    def test_fuzzy_search_by_accessories(self):
        response = self.client.get("/devices/devices/", {"search": "AccD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_donor(self):
        response = self.client.get("/devices/devices/", {"search": "Donor1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["donor"] == "Donor1" for result in results))

    def test_fuzzy_search_by_donor(self):
        response = self.client.get("/devices/devices/", {"search": "Donr1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_date_of_donation(self):
        response = self.client.get("/devices/devices/", {"search": "2019-04-01"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["date_of_donation"] == "2019-04-01" for result in results)
        )

    def test_fuzzy_search_by_date_of_donation(self):
        response = self.client.get("/devices/devices/", {"search": "2019-04"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_value(self):
        response = self.client.get("/devices/devices/", {"search": "200"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["value"] == 200 for result in results))

    def test_fuzzy_search_by_value(self):
        response = self.client.get("/devices/devices/", {"search": "20"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_location(self):
        response = self.client.get("/devices/devices/", {"search": "Location1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["location"] == "Location1" for result in results))

    def test_fuzzy_search_by_location(self):
        response = self.client.get("/devices/devices/", {"search": "Loca1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_created_by(self):
        response = self.client.get("/devices/devices/", {"search": "User1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["created_by"] == "User1" for result in results))

    def test_fuzzy_search_by_created_by(self):
        response = self.client.get("/devices/devices/", {"search": "Us1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_status(self):
        response = self.client.get("/devices/devices/", {"search": "In Use"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["status"] == "In Use" for result in results))

    def test_fuzzy_search_by_status(self):
        response = self.client.get("/devices/devices/", {"search": "In Us"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_distributor(self):
        response = self.client.get("/devices/devices/", {"search": "DistributorA"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["distributor"] == "DistributorA" for result in results)
        )

    def test_fuzzy_search_by_distributor(self):
        response = self.client.get("/devices/devices/", {"search": "DistribuorA"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_warranty_service_info(self):
        response = self.client.get("/devices/devices/", {"search": "Warranty1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(
            all(result["warranty_service_info"] == "Warranty1" for result in results)
        )

    def test_fuzzy_search_by_warranty_service_info(self):
        response = self.client.get("/devices/devices/", {"search": "Warrnty1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_search_by_notes(self):
        response = self.client.get("/devices/devices/", {"search": "NotesD"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)
        self.assertTrue(all(result["notes"] == "NotesD" for result in results))

    def test_fuzzy_search_by_notes(self):
        response = self.client.get("/devices/devices/", {"search": "Notes"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertGreater(len(results), 0)

    def test_no_results_found(self):
        response = self.client.get("/devices/devices/", {"search": "NonExistent"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.json()["results"]
        self.assertEqual(len(results), 0)
