from django.shortcuts import render

from .models import Location, Profile, UserAgent, Search
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from .models import Device, Search
from .resources import DeviceResource, SearchResource
from import_export.formats.base_formats import CSV


def index(request):
    return render(request, 'appiumng/index.html')


def manual_task(request):
    id = request.GET.get('search_id')
    mode = request.GET.get('mode')
    if mode == 'list':
        return redirect(f'/admin/appiumng/search/')
    else:
        return redirect(f'/admin/appiumng/search/{id}/change/')
    
def export_view(request, pk):
    device = get_object_or_404(Device, pk=pk)
    resource = DeviceResource()
    dataset = resource.export(queryset=Device.objects.filter(name=device.name))
    response = HttpResponse(dataset.csv, content_type=CSV().get_content_type())
    response['Content-Disposition'] = f'attachment; filename="{device.name}.csv"'
    return response

def export_view(request, pk):
    device = get_object_or_404(Device, pk=pk)
    print(device)
    resource = SearchResource()
    dataset = resource.export(queryset=Search.objects.filter(Device=device))
    # 項目を指定 Location.nameを入れる

    response = HttpResponse(dataset.csv, content_type=CSV().get_content_type())
    response['Content-Disposition'] = f'attachment; filename="{device.name}.csv"'
    return response

def import_view(request, pk):
    if request.method == 'POST':
        file = request.FILES['import_file']
        device = get_object_or_404(Device, pk=pk)
        resource = SearchResource()

        # CSVデータをパースする
        dataset = CSV().create_dataset(file.read().decode('utf-8'))
        errors = []

        # 各行を検証
        for row in dataset.dict:
            error = False
            # 位置情報の一致を確認
            location_name = row['Location Name']
            if location_name:
                try:
                    location = Location.objects.get(name=location_name)
                except Location.DoesNotExist:
                    error = True
                    errors.append(f"Location not found: {location_name}")
                    continue
            # ユーザーエージェントの一致を確認
            user_agent_name = row['User Agent']
            if user_agent_name:
                try:
                    user_agent = UserAgent.objects.get(user_agent=user_agent_name)
                except UserAgent.DoesNotExist:
                    error = True
                    errors.append(f"UserAgent not found: {user_agent_name}")
                    continue

            # deviceの一致を確認
            device_name = row['Device Name']    
            device = None
            if device_name:
                try:
                    device = Device.objects.get(name=device_name)
                except Device.DoesNotExist:
                    error = True
                    errors.append(f"Device not found: {device_name}")
                    continue

            if not error:
                search = Search(pk=row.get('id'))
                search.Device = device
                search.location = location
                search.user_agent = user_agent
                search.search = row['search']
                search.count_by_day = row['count_by_day']
                search.rest_time = row['rest_time']
                search.save()


        # エラーがある場合、エラーメッセージを表示
        if errors:
            return render(request, 'admin/appiumng/device/import_form.html', {'device': device, 'errors': errors})

        # データをインポート
        resource.import_data(dataset, dry_run=True)  # Perform import
        return HttpResponse("Import successful")

    device = get_object_or_404(Device, pk=pk)
    return render(request, 'admin/appiumng/device/import_form.html', {'device': device})