# Generated by Django 4.2.4 on 2024-06-19 12:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appiumng', '0004_device'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='device',
            name='udid',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='searchresult',
            name='Device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appiumng.device'),
        ),
    ]
