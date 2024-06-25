from django.contrib import admin
from django.urls import path
from .views import index, manual_task,  export_view, import_view

urlpatterns = [
    path('manualtask/', manual_task),
    path('export/<int:pk>/', export_view, name='admin:appiumng_device_export'),
    path('import/<int:pk>/', import_view, name='admin:appiumng_device_import'),
    path('', index),
]
