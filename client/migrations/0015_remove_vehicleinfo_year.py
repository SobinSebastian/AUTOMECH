# Generated by Django 5.0.1 on 2024-02-10 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0014_serviceprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicleinfo',
            name='year',
        ),
    ]
