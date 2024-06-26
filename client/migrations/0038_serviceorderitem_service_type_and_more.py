# Generated by Django 5.0.1 on 2024-04-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0037_servicerecommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorderitem',
            name='service_type',
            field=models.CharField(choices=[('normal', 'Normal'), ('rsa', 'Rsa')], default='normal', max_length=20),
        ),
        migrations.AlterField(
            model_name='roadsideassistance',
            name='status',
            field=models.CharField(choices=[('requested', 'Requested'), ('accepted', 'Accepted'), ('At Location', 'At Location'), ('processing', 'Processing'), ('completed', 'Completed')], default='requested', max_length=20),
        ),
    ]
