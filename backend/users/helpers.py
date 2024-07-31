from django.core.exceptions import ValidationError


def getDefaultPermissions():
    return []


def getAllPermissions():
    return [
        "readDevices",
        "createDevices",
        "editDevices",
        "deleteDevices",
        "scanDevices",
        "bulkUploadDevices",
        "manageWarehouses",
        "manageDonors",
        "generateQRCodes",
    ]


def getValidPermissions(request_data, existing_permissions=None):
    permissions = request_data.get("permissions")


def updatePermissions(instance, new_permissions, operation="add"):
    if operation == "add":
        instance.permissions = list(set(instance.permissions).union(new_permissions))
    elif operation == "replace":
        instance.permissions = new_permissions
    elif operation == "remove":
        instance.permissions = [
            perm for perm in instance.permissions if perm not in new_permissions
        ]
    elif operation == "clear":
        instance.permissions = []
    else:
        raise ValueError("Invalid operation.")
    instance.save()
