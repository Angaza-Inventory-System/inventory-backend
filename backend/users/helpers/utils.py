"""
This module defines the `allPermissions` list, which contains all possible permissions for the application.

**allPermissions** (list of str): 
    A list of permission strings that define various levels of access within the application. 

**Permissions include:**
- `"readDevices"`: Permission to read device information.
- `"createDevices"`: Permission to create new device records.
- `"editDevices"`: Permission to edit existing device records.
- `"deleteDevices"`: Permission to delete device records.
- `"scanDevices"`: Permission to scan devices.
- `"bulkUploadDevices"`: Permission to upload multiple devices in bulk.
- `"manageWarehouses"`: Permission to manage warehouse information.
- `"manageDonors"`: Permission to manage donor information.
- `"manageShipments"`: Permission to manage shipment information.
- `"generateQRCodes"`: Permission to generate QR codes for devices or shipments.
"""

allPermissions = [
    "readDevices",
    "createDevices",
    "editDevices",
    "deleteDevices",
    "scanDevices",
    "bulkUploadDevices",
    "manageWarehouses",
    "manageDonors",
    "manageShipments",
    "generateQRCodes",
]
