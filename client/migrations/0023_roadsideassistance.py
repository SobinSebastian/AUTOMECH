# Generated by Django 5.0.1 on 2024-02-21 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0022_serviceorder_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoadsideAssistance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('status', models.CharField(choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('processing', 'Processing'), ('completed', 'Completed')], max_length=20)),
                ('slug', models.CharField(max_length=36, unique=True)),
                ('description', models.TextField()),
                ('service_center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.servicecenter')),
                ('vehicle_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.vehicleinfo')),
            ],
        ),
    ]
