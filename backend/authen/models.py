from django.db import models

from backend.users.models import User


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
