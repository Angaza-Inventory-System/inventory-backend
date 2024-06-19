from django.db import models
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(models.Model):
 """
Attributes:
    user_id (int): The unique identifier for the user.
    username (str): The username of the user.
        - Constraints:
            - Must be between 2 and 50 characters in length.

    password (str): The password of the user.
        - Constraints:
            - Must be between 10 and 128 characters in length.
            - Must include at least one digit, one special character (!@#$%^&*), and one uppercase letter.

    email (str): The email address of the user.
        - Constraints:
            - Must be a valid email format.

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
        help_text=_("Minimum Length: 2 Characters. Maximum length: 50 Characters.")
    )
 password_validator = RegexValidator(
        regex='^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[A-Z]).{10,128}$', #AI Generated Regex
        message=_("Password must be at least 10 characters long and include at least one digit, one special character, and one uppercase letter.")
    )
 password = models.CharField(
        max_length=128,
        validators=[password_validator],
        help_text=_("Minimum Length: 10 Characters. Maximum Length: 128 Characters.")
    )
 email = models.EmailField(
        unique=True,
        db_index=True,
        validators=[EmailValidator()],          #AI Generated Line
        help_text=_("Must be a valid Email.")
    )
 role = models.CharField(
        max_length=50,
        validators=[MinLengthValidator(2)],
        help_text=_("Minimum Length: 2 Characters. Maximum Length: 50 Characters.")
    )
 first_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
        help_text=_("Minimum Length: 2 Characters. Maximum Length: 30 Characters.")
    )
 last_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2)],
        help_text=_("Minimum Length: 2 Characters. Maximum Length: 30 Characters.")
    )
