Here's the updated README with the additional user management URL information included:

# Backend

## Installation

To install the required packages, run the following command in a virtual environment:

```bash
pip install -r requirements.txt
```

## Development

To start the backend system, run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

## Django Apps

So far, the backend system consists of four Django apps:

1. **authen**:
    - Handles user authentication and authorization.
    - Implements multi-factor authentication.

2. **devices**:
    - Manages device metadata, including CRUD operations.

3. **users**:
    - Endpoints for user management and permission verification.
    - Implements role-based access control.

4. **admin** (TODO):
    - Manages user accounts and roles.

## API Endpoints

### User Endpoints

- **`GET {{base_url}}/users/users/`**
  - List all users.
- **`POST {{base_url}}/users/users/`**
  - Create a new user.
- **`GET {{base_url}}/users/users/{id}/`**
  - Retrieve a specific user.
- **`PUT {{base_url}}/users/users/{id}/`**
  - Update a specific user.
- **`PATCH {{base_url}}/users/users/{id}/`**
  - Partially update a specific user.
- **`DELETE {{base_url}}/users/users/{id}/`**
  - Delete a specific user.

### User Registration

- **`POST {{base_url}}/users/register/`**
  - Register a new user. This endpoint is for user creation and registration.

### User Password Update

- **`PATCH {{base_url}}/users/password/`**
  - Update the password of the currently authenticated user.

### User Permissions Endpoints

- **`GET {{base_url}}/users/user-permissions/<str:username>/`**
  - Retrieve permissions for a specific user by username.
- **`PATCH {{base_url}}/users/user-permissions/<str:username>/`**
  - Partially update permissions for a specific user by username.
- **`PUT {{base_url}}/users/user-permissions/<str:username>/`**
  - Update all permissions for a specific user by username.
- **`DELETE {{base_url}}/users/user-permissions/<str:username>/`**
  - Delete a specific user's permissions by username.
- **`DELETE {{base_url}}/users/user-permissions/<str:username>/clear/`**
  - Remove all permissions for a specific user by username.

### Device Endpoints

- **`GET {{base_url}}/inventory/devices/`**
  - List all devices.
- **`POST {{base_url}}/inventory/devices/`**
  - Create a new device.
- **`GET {{base_url}}/inventory/devices/{id}/`**
  - Retrieve a specific device.
- **`PUT {{base_url}}/inventory/devices/{id}/`**
  - Update a specific device.
- **`PATCH {{base_url}}/inventory/devices/{id}/`**
  - Partially update a specific device.
- **`DELETE {{base_url}}/inventory/devices/{id}/`**
  - Delete a specific device.

### Location Endpoints

- **`GET {{base_url}}/inventory/locations/`**
  - List all locations.
- **`POST {{base_url}}/inventory/locations/`**
  - Create a new location.
- **`GET {{base_url}}/inventory/locations/{id}/`**
  - Retrieve a specific location.
- **`PUT {{base_url}}/inventory/locations/{id}/`**
  - Update a specific location.
- **`PATCH {{base_url}}/inventory/locations/{id}/`**
  - Partially update a specific location.
- **`DELETE {{base_url}}/inventory/locations/{id}/`**
  - Delete a specific location.

### Donor Endpoints

- **`GET {{base_url}}/inventory/donors/`**
  - List all donors.
- **`POST {{base_url}}/inventory/donors/`**
  - Create a new donor.
- **`GET {{base_url}}/inventory/donors/{id}/`**
  - Retrieve a specific donor.
- **`PUT {{base_url}}/inventory/donors/{id}/`**
  - Update a specific donor.
- **`PATCH {{base_url}}/inventory/donors/{id}/`**
  - Partially update a specific donor.
- **`DELETE {{base_url}}/inventory/donors/{id}/`**
  - Delete a specific donor.

### Shipment Endpoints

- **`GET {{base_url}}/inventory/shipments/`**
  - List all shipments.
- **`POST {{base_url}}/inventory/shipments/`**
  - Create a new shipment.
- **`GET {{base_url}}/inventory/shipments/{id}/`**
  - Retrieve a specific shipment.
- **`PUT {{base_url}}/inventory/shipments/{id}/`**
  - Update a specific shipment.
- **`PATCH {{base_url}}/inventory/shipments/{id}/`**
  - Partially update a specific shipment.
- **`DELETE {{base_url}}/inventory/shipments/{id}/`**
  - Delete a specific shipment.

### Batch Operations

- **`POST {{base_url}}/inventory/batch/`**
  - Perform batch operations (create, update, or delete) on records for devices, donors, locations, or shipments.

### Mock Data Generation

- **`POST {{base_url}}/inventory/generate-mock-data/`**
  - Populate the database with sample data for testing purposes.
