# Generated by Django 3.0.5 on 2020-08-12 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='key',
            field=models.CharField(max_length=200),
        ),
    ]