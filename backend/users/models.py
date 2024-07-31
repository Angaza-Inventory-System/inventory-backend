"""Custom user model for application-specific user management."""

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MinLengthValidator, RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from .helpers import getAllPermissions, getDefaultPermissions
from .validators import validate_permissions


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Create and save a regular user with the given email and password.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.
            password (str, optional): The password for the new user. Defaults to None.
            **extra_fields: Any additional fields to be saved in the user model.

        Returns:
            User: The newly created user instance.
        """
        if not email:
            raise ValueError(_("The Email field must be set"))
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Create and save a superuser with the given email and password.

        Args:
            username (str): The username for the new user.
            email (str): The email address for the new user.
            password (str, optional): The password for the new user. Defaults to None.
            **extra_fields: Any additional fields to be saved in the user model.

        Returns:
            User: The newly created superuser instance.
        """
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model for application-specific user management.

    Inherits from:
        - AbstractBaseUser: Base class for implementing a custom user model.
        - PermissionsMixin: Provides the methods and fields necessary for handling permissions.

    Attributes:
        username (str): The username of the user.
            - Constraints:
                - Must be between 2 and 50 characters in length.

        password (str): The hashed password of the user.
            - Constraints:
                - Automatically hashed using Django's make_password method.
                - Must be between 10 and 128 characters in length.
                - Must include at least one digit, one special character (!@#$%^&*), and one uppercase letter.

        email (str): The email address of the user.
            - Constraints:
                - Must be a valid email format.
                - Must be unique across users.

        role (str): The role of the user.
            - Constraints:
                - Must be between 2 and 50 characters in length.

        first_name (str): The first name of the user.
            - Constraints:
                - Must be between 2 and 30 characters in length.

        last_name (str): The last name of the user.
            - Constraints:
                - Must be between 2 and 30 characters in length.
    """

    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[MinLengthValidator(2)],
        help_text=_("Minimum Length: 2 Characters. Maximum length: 50 Characters."),
    )
    password = models.CharField(
        max_length=128,
    )
    email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],
    )
    role = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
    )
    first_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
    )
    last_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
    )

    permissions = models.JSONField(
        default=getDefaultPermissions(),
        blank=False,
    )

    is_superuser = models.BooleanField(
        default=False,
    )

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email", "role", "first_name", "last_name", "password"]

    def clean(self):
        super().clean()
        # Perform permissions validation
        validate_permissions(self.permissions, self)

        if self.is_superuser:
            self.permissions = getAllPermissions()

        # Password validation
        password_validator = RegexValidator(
            regex="^(?=.*\\d)(?=.*[!@#$%^&*])(?=.*[A-Z]).{10,128}$",
            message=_(
                "Password must be at least 10 characters long and include at least one digit, one special character, and one uppercase letter."
            ),
        )
        try:
            password_validator(self.password)
        except ValidationError as e:
            raise ValidationError({"password": e.message})

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
