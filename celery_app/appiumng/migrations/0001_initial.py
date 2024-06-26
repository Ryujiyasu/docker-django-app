# Generated by Django 4.2.4 on 2024-05-21 13:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('profile_sum', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_agent', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search', models.CharField(max_length=200)),
                ('rest_time', models.IntegerField(default=0)),
                ('count_by_day', models.IntegerField(default=0)),
                ('location', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appiumng.location')),
                ('user_agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appiumng.useragent')),
            ],
        ),
    ]
