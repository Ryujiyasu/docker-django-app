# Generated by Django 4.2.4 on 2024-06-23 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appiumng', '0011_device_host'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='host',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
