# Backend

## Installation

To install the required packages, run the following command in a virtual environment:

```bash
pip install -r requirements.txt
```

## Development

To start the backend system, run the following command:

```bash
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

-   `/devices/`

    -   GET: Gets all devices
    -   POST with body: creates a new device

-   `/devices/warehouse/`

    -   GET: Gets all warehouses
    -   POST with body: creates a new warehouse

-   `/devices/donors/`

    -   GET: Gets all donors
    -   POST with body: creates a new donor

-   `/users/`

    -   GET: Gets all users
    -   POST with body: creates a new user

-   `/auth/`

    -   GET: Gets all JWTs
    -   POST with body: creates a new token

-   `/devices/<id>/`

    -   PUT with body: updates device `<id>` with body
    -   DELETE: deletes device `<id>`

-   `/devices/warehouses/<id>/`

    -   PUT with body: updates warehouse `<id>` with body
    -   DELETE: deletes warehouse `<id>`

-   `/devices/donors/<id>/`

    -   PUT with body: updates donor `<id>` with body
    -   DELETE: deletes donor `<id>`

-   `/users/<id>/`

    -   PUT with body: updates user `<id>` with body
    -   DELETE: deletes user `<id>`

-   `/auth/<id>/`
    -   PUT with body: updates JWTs `<id>` with body
    -   DELETE: deletes JWToken `<id>`
