# Generated by Django 3.1.7 on 2021-03-25 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20210325_1509'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='type',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
