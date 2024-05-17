from django.db import models


class Sample(models.Model):              #追加
    attachment = models.FileField()      #追加