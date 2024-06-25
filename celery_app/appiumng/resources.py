from import_export import resources
from .models import Device, Search

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

class SearchResource(resources.ModelResource):
    class Meta:
        model = Search