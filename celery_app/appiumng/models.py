from django.db import models
from django.utils import timezone

# Create your models here.



class Location(models.Model):
    class Meta:
        verbose_name = '位置情報'
        verbose_name_plural = '位置情報'
    
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    class Meta:
        verbose_name = 'プロフィール数設定'
        verbose_name_plural = 'プロフィール数設定'
    date = models.DateField()
    profile_sum = models.IntegerField()
    Device = models.ForeignKey('Device', on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.date)
    
class Device(models.Model):
    name = models.CharField(max_length=200, unique=True)
    platform = models.CharField(max_length=200, choices=(('ios', 'iOS'), ('android', 'Android')))
    Profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    udid = models.CharField(max_length=200, null=True)
    profile_num = models.IntegerField(default=0)
    host = models.CharField(max_length=200, null=True)
    port = models.IntegerField(default=4723)
    system_port = models.IntegerField(default=8200)
    
    def __str__(self):
        return self.name

class UserAgent(models.Model):
    class Meta:
        verbose_name = 'UA設定'
        verbose_name_plural = 'UA設定'
    name = models.CharField(max_length=200)
    user_agent = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user_agent

class Search(models.Model):
    class Meta:
        verbose_name = '検索情報設定'
        verbose_name_plural = '検索情報設定'
    search = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    user_agent = models.ForeignKey(UserAgent, on_delete=models.CASCADE, null=True)
    rest_time = models.IntegerField(default=0)
    count_by_day = models.IntegerField(default=0)
    Device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return self.search

class SearchResult(models.Model):
    class Meta:
        verbose_name = '検索結果'
        verbose_name_plural = '検索結果'
    search = models.ForeignKey(Search, on_delete=models.CASCADE)
    datetime = models.DateTimeField()
    success = models.BooleanField()
    memo = models.TextField()
    Device = models.ForeignKey(Device, on_delete=models.CASCADE, null=True)
    ip = models.GenericIPAddressField(null=True)
    
    def __str__(self):
        #日本時間で表示

        return f'{self.search} {self.datetime.astimezone(timezone.get_current_timezone()).strftime("%Y-%m-%d %H:%M:%S")} {self.success}'



