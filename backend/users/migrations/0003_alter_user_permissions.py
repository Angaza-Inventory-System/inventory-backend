# Generated by Django 5.0.7 on 2024-07-27 01:16

from django.db import migrations, models

import backend.users.models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_remove_user_is_active_remove_user_is_staff"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="permissions",
            field=models.JSONField(
                default=backend.users.models.get_default_permissions
            ),
        ),
    ]
