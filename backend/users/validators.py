from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .helpers import getAllPermissions


def validate_permissions(value):
    """
    Validate that permissions is a list and only contains valid permissions.
    """
    all_permissions = set(
        [
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
    )

    if not isinstance(value, list):
        raise ValidationError(_("Permissions must be a list."))

    invalid_permissions = [perm for perm in value if perm not in all_permissions]

    if invalid_permissions:
        raise ValidationError(
            _("Invalid permissions: %s") % ", ".join(invalid_permissions)
        )

    if len(value) != len(set(value)):
        raise ValidationError(_("Permissions list must not contain duplicates."))
