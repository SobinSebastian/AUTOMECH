# Generated by Django 5.0.1 on 2024-02-08 16:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0013_alter_servicesslots_allocated_mech_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServicePrice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('slug', models.SlugField(editable=False, max_length=255, unique=True)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.servicelist')),
                ('variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.modelvariant')),
            ],
            options={
                'unique_together': {('variant', 'service')},
            },
        ),
    ]
