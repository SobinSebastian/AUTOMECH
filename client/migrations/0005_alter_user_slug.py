# Generated by Django 5.0.1 on 2024-02-04 11:53

from django.db import migrations, models
from django.utils.text import slugify

def update_slugs(apps, schema_editor):
    User = apps.get_model('client', 'User')
    for user in User.objects.all():
        base_slug = slugify(user.first_name)
        unique_slug = base_slug
        counter = 1
        while User.objects.filter(slug=unique_slug).exclude(pk=user.pk).exists():
            unique_slug = f"{base_slug}-{counter}"
            counter += 1
        user.slug = unique_slug
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_manager_user_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.RunPython(update_slugs),
    ]