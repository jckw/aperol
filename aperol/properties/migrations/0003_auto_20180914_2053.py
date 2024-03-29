# Generated by Django 2.1 on 2018-09-14 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0002_auto_20180903_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='total_price',
            field=models.IntegerField(default=2000, verbose_name='Total price per month for all tenants'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='property',
            name='price',
            field=models.IntegerField(verbose_name='Minimum price per month per person'),
        ),
    ]
