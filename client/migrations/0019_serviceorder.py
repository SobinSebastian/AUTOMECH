# Generated by Django 5.0.1 on 2024-02-18 16:17

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0018_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('slug', models.SlugField(default=uuid.uuid4, editable=False, max_length=36, unique=True)),
                ('service_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.servicecenter')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vehicleinfo')),
            ],
        ),
    ]