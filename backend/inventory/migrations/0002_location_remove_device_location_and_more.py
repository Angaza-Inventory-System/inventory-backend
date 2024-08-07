# Generated by Django 5.0.7 on 2024-08-02 01:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("inventory", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Location",
            fields=[
                ("location_id", models.AutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=100)),
                ("address", models.TextField(max_length=500)),
                ("country", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=100)),
                ("postal_code", models.CharField(max_length=20)),
                ("phone", models.CharField(blank=True, max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name="device",
            name="location",
        ),
        migrations.RemoveField(
            model_name="device",
            name="accessories",
        ),
        migrations.RemoveField(
            model_name="device",
            name="distributor",
        ),
        migrations.RemoveField(
            model_name="device",
            name="shipment_date",
        ),
        migrations.RemoveField(
            model_name="device",
            name="status",
        ),
        migrations.RemoveField(
            model_name="device",
            name="warranty_service_info",
        ),
        migrations.AlterField(
            model_name="device",
            name="mac_id",
            field=models.CharField(
                blank=True, db_index=True, max_length=100, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="device",
            name="specifications",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="device",
            name="end_location",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="received_items",
                to="inventory.location",
            ),
        ),
        migrations.AddField(
            model_name="device",
            name="start_location",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="stored_items",
                to="inventory.location",
            ),
        ),
        migrations.CreateModel(
            name="Shipping",
            fields=[
                ("shipping_id", models.AutoField(primary_key=True, serialize=False)),
                ("arrived", models.BooleanField(default=False)),
                ("date_shipped", models.DateField()),
                ("date_delivered", models.DateField(null=True)),
                ("tracking_identifier", models.CharField(blank=True, max_length=100)),
                (
                    "destination",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="destination_shipments",
                        to="inventory.location",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="device",
            name="shipping_infos",
            field=models.ManyToManyField(
                blank=True, related_name="devices", to="inventory.shipping"
            ),
        ),
        migrations.DeleteModel(
            name="Warehouse",
        ),
    ]
