# Generated by Django 2.2.5 on 2019-12-08 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0018_auto_20191208_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hkstockstaticinfo',
            name='short_name',
            field=models.CharField(max_length=4),
        ),
    ]
