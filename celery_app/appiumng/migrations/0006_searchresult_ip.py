# Generated by Django 4.2.4 on 2024-06-19 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appiumng', '0005_device_active_device_udid_searchresult_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchresult',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]