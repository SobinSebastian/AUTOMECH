# Generated by Django 5.0.1 on 2024-01-21 02:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0006_transmissiontype'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelvariant',
            name='transmission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.transmissiontype'),
        ),
    ]
