# Generated by Django 5.0.1 on 2024-03-16 23:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0032_roadsideassistance_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roadsideassistance',
            name='created_at',
        ),
    ]
