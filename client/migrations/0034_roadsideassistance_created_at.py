# Generated by Django 5.0.1 on 2024-03-16 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0033_remove_roadsideassistance_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadsideassistance',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
