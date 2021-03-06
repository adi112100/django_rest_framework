# Generated by Django 3.0.5 on 2020-08-14 10:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hashid', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=200)),
                ('title', models.CharField(max_length=200)),
                ('blog', models.TextField(default='')),
                ('time', models.DateTimeField(default=datetime.datetime.today)),
                ('status', models.CharField(default='0', max_length=200)),
                ('key', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('college', models.CharField(max_length=200)),
                ('branch', models.CharField(max_length=200)),
                ('fullname', models.CharField(max_length=200)),
                ('hashkey', models.CharField(default='', max_length=200)),
            ],
        ),
    ]
