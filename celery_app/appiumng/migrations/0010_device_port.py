# Generated by Django 4.2.4 on 2024-06-23 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appiumng', '0009_device_profile_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='port',
            field=models.IntegerField(default=4723),
        ),
    ]
