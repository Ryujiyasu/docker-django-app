# Generated by Django 4.2.4 on 2024-06-23 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appiumng', '0010_device_port'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='host',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
