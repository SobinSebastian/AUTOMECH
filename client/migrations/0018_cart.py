# Generated by Django 5.0.1 on 2024-02-18 05:25

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0017_modelvariant_variant_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.servicelist')),
                ('vehicle_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vehicleinfo')),
            ],
            options={
                'unique_together': {('client', 'vehicle_info', 'service_list')},
            },
        ),
    ]
