# Generated by Django 4.2.4 on 2024-06-21 05:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appiumng', '0006_searchresult_ip'),
    ]

    operations = [
        migrations.AddField(
            model_name='search',
            name='Device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appiumng.device'),
        ),
    ]
