# Generated by Django 5.0.7 on 2024-08-01 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
