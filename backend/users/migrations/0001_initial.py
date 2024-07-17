# Generated by Django 4.2.13 on 2024-07-16 08:55

import backend.users.fields
import backend.users.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(help_text='Minimum Length: 2 Characters. Maximum length: 50 Characters.', max_length=50, unique=True, validators=[django.core.validators.MinLengthValidator(2)])),
                ('password', models.CharField(help_text='Minimum Length: 10 Characters. Maximum Length: 128 Characters.', max_length=128, validators=[django.core.validators.RegexValidator(message='Password must be at least 10 characters long and include at least one digit, one special character, and one uppercase letter.', regex='^(?=.*\\d)(?=.*[!@#$%^&*])(?=.*[A-Z]).{10,128}$')])),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, validators=[django.core.validators.EmailValidator()])),
                ('role', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)])),
                ('first_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('last_name', models.CharField(max_length=30, validators=[django.core.validators.MinLengthValidator(2)])),
                ('permissions', backend.users.fields.EncryptedJSONField(default={'bulkUploadDevices': False, 'createDevices': False, 'deleteDevices': False, 'editDevices': False, 'generateQRCodes': False, 'manageDonors': False, 'manageWarehouses': False, 'readDevices': False, 'scanDevices': False}, validators=[backend.users.validators.validate_permissions])),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
