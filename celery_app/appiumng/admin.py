from django.contrib import admin
from .models import Location, Profile, UserAgent, Search
# Register your models here.


admin.site.register(Location)
admin.site.register(Profile)
admin.site.register(UserAgent)
admin.site.register(Search)
