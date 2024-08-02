from haystack import indexes

from .models import Device, Donor, Location


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
    warehouse_number = indexes.CharField(model_attr="warehouse_number")
    name = indexes.CharField(model_attr="name")
    country = indexes.CharField(model_attr="country")
    city = indexes.CharField(model_attr="city")
    postal_code = indexes.CharField(model_attr="postal_code")
    phone = indexes.CharField(model_attr="phone")

    @staticmethod
    def get_model():
        return Location

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
