# Generated by Django 5.0.1 on 2024-03-09 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0028_task_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceorder',
            name='razorpay_order_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='razorpay_payment_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='serviceorder',
            name='razorpay_signature',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]