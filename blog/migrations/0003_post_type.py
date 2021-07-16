# Generated by Django 3.1.7 on 2021-03-25 14:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0002_post_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='type',
            field=models.ManyToManyField(related_name='post_type', to=settings.AUTH_USER_MODEL),
        ),
    ]