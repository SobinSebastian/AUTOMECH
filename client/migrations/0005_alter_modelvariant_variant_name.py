# Generated by Django 5.0.1 on 2024-01-20 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_modelvariant_variant_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelvariant',
            name='variant_name',
            field=models.CharField(max_length=50),
        ),
    ]
