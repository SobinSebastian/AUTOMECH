# Generated by Django 5.0.1 on 2024-02-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0011_alter_servicesslots_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesslots',
            name='status',
            field=models.CharField(choices=[('FREE', 'Free'), ('ALLOCATED', 'Allocated'), ('ACTIVE', 'Active'), ('INACTIVE', 'Inactive')], default='INACTIVE', max_length=50),
        ),
    ]