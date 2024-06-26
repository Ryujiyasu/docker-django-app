from django.contrib import admin
from django.utils.html import format_html
from .models import Location, Profile, UserAgent, Search, SearchResult, Device
from django.contrib import auth
from django.utils import timezone
from django.urls import path
import datetime
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .resources import SearchResource, DeviceResource
from .views import export_view, import_view

admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location

class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ('name', 'latitude', 'longitude')

    
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('datetime', "Device", 'success', 'colored_result')

    def colored_result(self, obj):
        color = 'red' if not obj.success else 'white'
        return format_html('<span style="color: {};">{}</span>', color, obj.search)
    colored_result.short_description = 'Result'




class SearchAdmin(ImportExportModelAdmin):
    resource_class = SearchResource
    list_display = ('search', 'Device', 'location', 'user_agent', 'count_by_day', 'rest_time', 'today_results','all_results', 'manual_task_submit_from_list' )

    def get_changeform_initial_data(self, request):
        deviceId = request.GET.get('device')
        if deviceId:
            return {
                'Device': deviceId
            }

    def today_results(self, obj):
        # 本日の検索結果を取得
        results = obj.searchresult_set.filter(datetime__date=datetime.datetime.now().date())
        
        # 失敗があれば赤色で表示
        if len([result for result in results if not result.success]) > 0:
            return format_html('<span style="color: red;">{}</span>', f'{len([result for result in results if result.success])}/{len(results)}')
        else:
            return f'{len([result for result in results if result.success])}/{len(results)}'
    today_results.short_description = '本日の検索回数'

    def all_results(self, obj):
        results = obj.searchresult_set.all()
        
        return f'{len([result for result in results if result.success])}/{len(results)}'
    all_results.short_description = '総検索回数'
    
    readonly_fields = ['today_results_list','all_results_list','manual_task_submit']
    
    
    def manual_task_submit_from_list(self, obj):
        return format_html('<a href="/appiumng/manualtask/?search_id={}&mode=list">手動タスク実行</a>', obj.id)
    
    manual_task_submit_from_list.short_description = '手動タスク実行'
    
    
    def manual_task_submit(self, obj):
        return format_html('<a href="/appiumng/manualtask/?search_id={}">手動タスク実行</a>', obj.id)
    
    manual_task_submit.short_description = '手動タスク実行'
    
    def today_results_list(self, obj):
        results = obj.searchresult_set.filter(datetime__date=datetime.datetime.now().date())
        links = []
        for result in results:
            url = f"/admin/appiumng/searchresult/{result.id}/change/"
            color = 'red' if not result.success else 'black'
            links.append(format_html('<a href="{}" style="color: {};">{}</a>', url, color, str(result)))
        return format_html("<br>".join(links))
    today_results_list.short_description = '本日の検索結果'

    def all_results_list(self, obj):
        results = obj.searchresult_set.all()
        links = []
        for result in results:
            url = f"/admin/appiumng/searchresult/{result.id}/change/"
            color = 'red' if not result.success else 'black'
            links.append(format_html('<a href="{}" style="color: {};">{}</a>', url, color, str(result)))
        return format_html("<br>".join(links))
    all_results_list.short_description = '総検索結果'

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('date', 'profile_sum', 'Device')
    list_filter = ('Device',)
    search_fields = ('date', 'profile_sum', 'Device')

class DeviceAdmin(ImportExportModelAdmin):
    resource_class = DeviceResource

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['opts'] = self.model._meta
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                '<path:object_id>/export/',
                self.admin_site.admin_view(self.export_view),
                name='appiumng_device_export',
            ),
            path(
                '<path:object_id>/import/',
                self.admin_site.admin_view(self.import_view),
                name='appiumng_device_import',
            ),
        ]
        return custom_urls + urls

    def export_view(self, request, object_id, *args, **kwargs):
    
        return export_view(request, object_id)

    def import_view(self, request, object_id, *args, **kwargs):
        return import_view(request, object_id)

admin.site.register(Location,LocationAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserAgent)
admin.site.register(Search, SearchAdmin)
admin.site.register(SearchResult,SearchResultAdmin)
admin.site.register(Device, DeviceAdmin)
