from django.shortcuts import render

from .models import Location, Profile, UserAgent, Search
from django.shortcuts import redirect

def index(request):
    return render(request, 'appiumng/index.html')


def manual_task(request):
    id = request.GET.get('search_id')
    mode = request.GET.get('mode')
    if mode == 'list':
        return redirect(f'/admin/appiumng/search/')
    else:
        return redirect(f'/admin/appiumng/search/{id}/change/')