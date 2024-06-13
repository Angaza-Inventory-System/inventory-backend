from django.db import models


class User(models.Model):
    """
    Represents a user in the system.

    Attributes:
        user_id (int): The unique identifier for the user.
        username (str): The username of the user.
        password (str): The password of the user.
        email (str): The email address of the user.
        role (str): The role of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
    """

    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(max_length=50)  # TODO: Connect to a Role model
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class JWTToken(models.Model):
    """
    Model representing a JWT token.

    Attributes:
        token_id (AutoField): The primary key for the token.
        user (ForeignKey): The user associated with the token.
        token (TextField): The actual token value.
        created_at (DateTimeField): The timestamp when the token was created.
        expires_at (DateTimeField): The timestamp when the token expires.
        is_blacklisted (BooleanField): Indicates if the token is blacklisted.
    """

    token_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_blacklisted = models.BooleanField(default=False)
