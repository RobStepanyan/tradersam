# Generated by Django 2.2.7 on 2019-12-08 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0020_auto_20191208_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hkstockstaticinfo',
            name='long_name',
            field=models.CharField(max_length=75),
        ),
    ]
