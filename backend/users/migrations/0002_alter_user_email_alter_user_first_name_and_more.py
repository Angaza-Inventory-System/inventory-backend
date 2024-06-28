# Generated by Django 5.0.6 on 2024-06-28 19:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                db_index=True,
                max_length=254,
                unique=True,
                validators=[django.core.validators.EmailValidator()],
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                max_length=30, validators=[django.core.validators.MinLengthValidator(2)]
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="last_name",
            field=models.CharField(
                max_length=30, validators=[django.core.validators.MinLengthValidator(2)]
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                max_length=50, validators=[django.core.validators.MinLengthValidator(2)]
            ),
        ),
    ]