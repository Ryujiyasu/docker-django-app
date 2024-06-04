from django.db import models

# Create your models here.



class Location(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    date = models.DateField()
    profile_sum = models.IntegerField()
    
    def __str__(self):
        return str(self.date)

class UserAgent(models.Model):
    user_agent = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user_agent

class Search(models.Model):
    search = models.CharField(max_length=200)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    user_agent = models.ForeignKey(UserAgent, on_delete=models.CASCADE, null=True)
    rest_time = models.IntegerField(default=0)
    count_by_day = models.IntegerField(default=0)
    
    def __str__(self):
        return self.search
    



