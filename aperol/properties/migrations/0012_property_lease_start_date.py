# Generated by Django 2.1 on 2018-09-28 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0011_property_lease_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='lease_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
