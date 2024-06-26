from import_export import resources
from .models import Device, Search
from import_export.fields import Field

class DeviceResource(resources.ModelResource):
    class Meta:
        model = Device

class SearchResource(resources.ModelResource):
    location_name = Field(attribute='location__name', column_name='Location Name')
    user_agent = Field(attribute='user_agent__user_agent', column_name='User Agent')
    device_name = Field(attribute='Device__name', column_name='Device Name')
    class Meta:
        model = Search
        fields = ('id',"device_name" ,"search",'location_name', 'user_agent', 'count_by_day', 'rest_time', 'today_results', 'all_results')