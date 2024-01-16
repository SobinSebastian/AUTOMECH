# Generated by Django 5.0.1 on 2024-01-15 09:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_userinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarMake',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('Model_Image', models.ImageField(blank=True, null=True, upload_to='model_images/')),
                ('make_company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.carmake')),
            ],
        ),
    ]