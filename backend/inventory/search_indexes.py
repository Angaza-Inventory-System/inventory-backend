"""
Search Indexes for the inventory management system.

This module defines search indexes for various models used in the inventory system, 
allowing full-text search functionality using Haystack.

Indexes:
- DeviceIndex: Indexes the Device model, including fields like device_id, type, make, model, 
  and other relevant attributes.
- DonorIndex: Indexes the Donor model, covering fields such as name, contact_info, address, 
  email, and phone.
- WarehouseIndex: Indexes the Location model (representing warehouses), including fields 
  like name, country, city, postal_code, and phone.
- ShipmentIndex: Indexes the Shipment model, capturing details like shipping_id, 
  destination_name, arrived status, date_shipped, date_delivered, and tracking_identifier.

Each index class inherits from Haystack's SearchIndex and Indexable, and defines the 
fields to be indexed and the queryset to be used for indexing. The `get_model()` 
method specifies the model to be indexed, and the `index_queryset()` method 
provides the queryset for the index.

Usage:
- These indexes enable full-text search capabilities for devices, donors, locations, and shipments 
  in the inventory system.
"""

from haystack import indexes
from .models import Device, Donor, Location, Shipment

class DeviceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    device_id = indexes.CharField(model_attr="device_id")
    type = indexes.CharField(model_attr="type")
    make = indexes.CharField(model_attr="make")
    model = indexes.CharField(model_attr="model")
    year_of_manufacture = indexes.IntegerField(model_attr="year_of_manufacture")
    status = indexes.CharField(model_attr="status")
    operating_system = indexes.CharField(model_attr="operating_system")
    physical_condition = indexes.CharField(model_attr="physical_condition")
    donor_name = indexes.CharField(model_attr="donor__name")
    location_name = indexes.CharField(model_attr="location__name")
    created_by_username = indexes.CharField(model_attr="created_by__username")
    mac_id = indexes.CharField(model_attr="mac_id")
    serial_number = indexes.CharField(model_attr="serial_number")

    @staticmethod
    def get_model():
        return Device

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class DonorIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    contact_info = indexes.CharField(model_attr="contact_info")
    address = indexes.CharField(model_attr="address")
    email = indexes.CharField(model_attr="email")
    phone = indexes.CharField(model_attr="phone")

    @staticmethod
    def get_model():
        return Donor

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class WarehouseIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr="name")
    country = indexes.CharField(model_attr="country")
    city = indexes.CharField(model_attr="city")
    postal_code = indexes.CharField(model_attr="postal_code")
    phone = indexes.CharField(model_attr="phone")

    @staticmethod
    def get_model():
        return Location  # Ensure this matches your actual model

    def index_queryset(self, using=None):
        return self.get_model().objects.all()

class ShipmentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    shipping_id = indexes.CharField(model_attr="shipping_id")
    destination_name = indexes.CharField(model_attr="destination__name")
    arrived = indexes.BooleanField(model_attr="arrived")
    date_shipped = indexes.DateField(model_attr="date_shipped")
    date_delivered = indexes.DateField(model_attr="date_delivered", null=True)
    tracking_identifier = indexes.CharField(model_attr="tracking_identifier")

    @staticmethod
    def get_model():
        return Shipment

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
