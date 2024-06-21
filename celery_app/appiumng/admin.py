from django.contrib import admin
from django.utils.html import format_html
from .models import Location, Profile, UserAgent, Search, SearchResult, Device
from django.contrib import auth
from django.utils import timezone
import datetime
from import_export import resources
from import_export.admin import ImportExportModelAdmin

admin.site.unregister(auth.models.User)
admin.site.unregister(auth.models.Group)

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location

class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ('name', 'latitude', 'longitude')

    
class SearchResultAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'success', 'colored_result')

    def colored_result(self, obj):
        color = 'red' if not obj.success else 'white'
        return format_html('<span style="color: {};">{}</span>', color, obj.search)
    colored_result.short_description = 'Result'





class SearchAdmin(admin.ModelAdmin):
    list_display = ('search', 'location', 'user_agent', 'count_by_day', 'rest_time', 'today_results','all_results', 'manual_task_submit_from_list' )

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
    
    today_results_list.short_description = '本日の検索結果一覧'
    
    
    def all_results_list(self, obj):
        results = obj.searchresult_set.all()
        links = []
        for result in results:
            url = f"/admin/appiumng/searchresult/{result.id}/change/"
            color = 'red' if not result.success else 'black'
            links.append(format_html('<a href="{}" style="color: {};">{}</a>', url, color, str(result)))
        return format_html("<br>".join(links))
    all_results_list.short_description = '総検索結果一覧'



admin.site.register(Location,LocationAdmin)
admin.site.register(Profile)
admin.site.register(UserAgent)
admin.site.register(Search, SearchAdmin)
admin.site.register(SearchResult,SearchResultAdmin)
admin.site.register(Device)
