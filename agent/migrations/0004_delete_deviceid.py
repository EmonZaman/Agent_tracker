# Generated by Django 3.2.5 on 2021-09-22 11:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agent', '0003_deviceid'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DeviceId',
        ),
    ]