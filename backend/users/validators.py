from django.core.exceptions import ValidationError


def validate_permissions(value, user):
    expected_keys = {
        "readDevices": bool,
        "createDevices": bool,
        "editDevices": bool,
        "deleteDevices": bool,
        "scanDevices": bool,
        "bulkUploadDevices": bool,
        "manageWarehouses": bool,
        "manageDonors": bool,
        "generateQRCodes": bool,
    }

    if not isinstance(value, dict):
        raise ValidationError("Permissions must be a dictionary.")

    for key, expected_type in expected_keys.items():
        if not isinstance(value[key], expected_type):
            raise ValidationError(
                f"Key '{key}' must be of type {expected_type.__name__}."
            )

    for key in value:
        if key not in expected_keys:
            raise ValidationError(f"Unexpected key: {key}")
