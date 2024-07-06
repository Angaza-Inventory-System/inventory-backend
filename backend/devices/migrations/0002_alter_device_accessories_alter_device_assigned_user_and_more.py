# Generated by Django 5.0.6 on 2024-06-28 19:00

import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("devices", "0001_initial"),
        ("users", "0002_alter_user_email_alter_user_first_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="device",
            name="accessories",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="assigned_user",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="assigned_devices",
                to="users.user",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="date_of_donation",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="date_received",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="device_id",
            field=models.UUIDField(
                default=uuid.uuid4, primary_key=True, serialize=False
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="distributor",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="donor",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="donated_devices",
                to="devices.donor",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="location",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stored_items",
                to="devices.warehouse",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="make",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="model",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="notes",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="operating_system",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="physical_condition",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="received_by",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="received_devices",
                to="users.user",
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="serial_number",
            field=models.CharField(db_index=True, max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="device",
            name="shipment_date",
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="specifications",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="status",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="type",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="device",
            name="value",
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name="device",
            name="warranty_service_info",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="device",
            name="year_of_manufacture",
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name="donor",
            name="address",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="donor",
            name="contact_info",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="donor",
            name="donor_id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="donor",
            name="email",
            field=models.EmailField(
                db_index=True,
                max_length=254,
                unique=True,
                validators=[django.core.validators.EmailValidator()],
            ),
        ),
        migrations.AlterField(
            model_name="donor",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="donor",
            name="phone",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="city",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="country",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="name",
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="phone",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="postal_code",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="warehouse",
            name="warehouse_number",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
