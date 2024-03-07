# Generated by Django 5.0.1 on 2024-03-06 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0026_post'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='servicelist',
            name='tasks',
            field=models.ManyToManyField(to='client.task'),
        ),
    ]
