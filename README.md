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

So far, the backend system consists of three Django apps:

1. authen:

    - Handles user authentication and authorization.
    - Implements multi-factor authentication.

2. devices:

    - Manages device metadata, including CRUD operations.

3. users:

    - Endpoints for permission verification.
    - Implements role-based access control.

4. admin (TODO):

    - Manages user accounts and roles.

## API Endpoints

-   `/users/`

    -   GET: Retrieve a list of all users

-   `/users/register/`

    -   POST: Create a new user.

-   `/users/<int:pk>/`

    -   PUT: Update details of a specific user.
    -   DELETE: Delete a specific user.

-   `/inventory/`

    -   GET: Retrieve a list of all devices with pagination and filtering.
    -   POST: Create a new device.

-   `/inventory/<uuid:pk>/`

    -   PUT: Update details of a specific device.
    -   DELETE: Delete a specific device.

-   `/inventory/locations/`

    -   GET: Retrieve a list of all locations.
    -   POST: Create a new location.

-   `/inventory/locations/<int:pk>/`

    -   PUT: Update details of a specific location.
    -   DELETE: Delete a specific location.

-   `/inventory/donors/`

    -   GET: Retrieve a list of all donors or create a new donor.
    -   POST: Create a new donor.

-   `/inventory/donors/<int:pk>/`

    -   PUT: Update details of a specific donor.
    -   DELETE: Delete a specific donor.

-   `/login/`
    -   POST: Authenticate a user and return a JWT
