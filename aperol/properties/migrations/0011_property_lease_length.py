# Generated by Django 2.1 on 2018-09-28 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0010_cityarea_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='lease_length',
            field=models.DurationField(blank=True, null=True),
        ),
    ]
