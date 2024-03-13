# Generated by Django 5.0.1 on 2024-03-12 22:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0030_serviceorder_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceorder',
            name='status',
            field=models.CharField(choices=[('on hold', 'On hold'), ('pending', 'Pending'), ('processing', 'Processing'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('closed', 'Closed')], default='on hold', max_length=20),
        ),
        migrations.AlterField(
            model_name='vehicleinfo',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
