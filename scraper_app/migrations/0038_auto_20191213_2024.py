# Generated by Django 2.2.7 on 2019-12-13 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0037_auto_20191213_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hkindexstaticinfo',
            name='long_name',
            field=models.CharField(max_length=56),
        ),
    ]
