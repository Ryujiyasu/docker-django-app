from django.contrib import admin
from django.urls import path
from .views import index, manual_task

urlpatterns = [
    path('manualtask/', manual_task),
    path('', index),
]
