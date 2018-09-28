# Generated by Django 2.1 on 2018-09-27 15:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0008_auto_20180925_0927'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='The variant name', max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='property',
            name='variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='properties.PropertyVariant'),
        ),
    ]