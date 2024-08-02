from .utils import allPermissions

def getValidPermissions(request_data):
    """
    Extracts and returns the permissions from the request data.

    **Parameters:**
    - `request_data` (dict): The request payload containing permission data.

    **Returns:**
    - List of permissions if present, otherwise returns `None`.
    """
    permissions = request_data.get("permissions")
    return permissions


def updatePermissions(instance, new_permissions, operation="add"):
    """
    Updates the permissions of a given instance based on the specified operation.

    **Parameters:**
    - `instance`: The object whose permissions will be updated.
    - `new_permissions` (list): The permissions to be added, replaced, removed, or cleared.
    - `operation` (str): The type of update operation. Options include:
        - `"add"`: Add new permissions.
        - `"replace"`: Replace existing permissions with new ones.
        - `"remove"`: Remove specified permissions.
        - `"clear"`: Clear all permissions.

    **Raises:**
    - `ValueError`: If an invalid operation is specified.

    **Returns:**
    - None
    """
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
