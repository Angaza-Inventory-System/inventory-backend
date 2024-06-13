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

1. auth:

-   Handles user authentication and authorization.
-   Implements multi-factor authentication.

2. devices:

-   Manages device metadata, including CRUD operations.

3. users:

-   Endpoints for permission verification.
-   Implements role-based access control.

4. admin (TODO):
-  Manages user accounts and roles.