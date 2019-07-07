# Generated by Django 2.2.3 on 2019-07-07 20:55

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0016_auto_20190707_2014'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='listing_url',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='bathrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='double_bedrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='ensuites',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='location',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='property',
            name='name',
            field=models.CharField(blank=True, help_text='Property number or name', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='single_bedrooms',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
