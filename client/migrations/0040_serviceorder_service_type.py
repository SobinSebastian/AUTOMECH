# Generated by Django 5.0.1 on 2024-04-02 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0039_remove_serviceorderitem_service_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='service_type',
            field=models.CharField(choices=[('normal', 'Normal'), ('rsa', 'Rsa')], default='normal', max_length=20),
        ),
    ]
