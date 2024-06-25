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
    dataset = resource.export(queryset=Device.objects.filter(pk=pk))
    response = HttpResponse(dataset.csv, content_type=CSV().get_content_type())
    response['Content-Disposition'] = f'attachment; filename="{device.name}.csv"'
    return response

def export_view(request, pk):
    device = get_object_or_404(Device, pk=pk)
    resource = DeviceResource()
    dataset = resource.export(queryset=Device.objects.filter(pk=pk))
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
            # デバイス名の一致を確認
            if row['Device'] != device.name:
                errors.append(f"Device name mismatch: {row['Device']} != {device.name}")
                continue

            # 位置情報の一致を確認
            location_name = row['location']
            if location_name:
                try:
                    location = Location.objects.get(name=location_name)
                except Location.DoesNotExist:
                    errors.append(f"Location not found: {location_name}")
                    continue

        # エラーがある場合、エラーメッセージを表示
        if errors:
            return render(request, 'admin/appiumng/device/import_form.html', {'device': device, 'errors': errors})

        # 古い検索ワードを削除
        Search.objects.filter(Device=device).delete()

        # データをインポート
        resource.import_data(dataset, dry_run=False)  # Perform import
        return HttpResponse("Import successful")

    device = get_object_or_404(Device, pk=pk)
    return render(request, 'admin/appiumng/device/import_form.html', {'device': device})