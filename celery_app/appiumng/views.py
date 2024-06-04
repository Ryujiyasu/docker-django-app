from django.shortcuts import render

from .models import Location, Profile, UserAgent, Search


def index(request):
    return render(request, 'appiumng/index.html')


