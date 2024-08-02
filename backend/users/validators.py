"""
Permission Validation Utility

This module provides a function to validate a list of permissions.

Function:

1. **validate_permissions(value)**
   - **Parameters:**
     - `value` (list): The list of permissions to validate.

   - **Raises:**
     - `ValidationError`: If `value` is not a list.
     - `ValidationError`: For any invalid permissions or duplicates in the list.

   - **Description:**
     - Checks if `value` is a list and contains only valid permissions without duplicates.
"""


from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .helpers.utils import allPermissions


def validate_permissions(value):
    """
    Validate that permissions is a list and only contains valid permissions.
    """

    if not isinstance(value, list):
        raise ValidationError(_("Permissions must be a list."))

    invalidPermissions = [perm for perm in value if perm not in allPermissions]

    if invalidPermissions:
        raise ValidationError(
            _("Invalid permissions: %s") % ", ".join(invalidPermissions)
        )

    if len(value) != len(set(value)):
        raise ValidationError(_("Permissions list must not contain duplicates."))
