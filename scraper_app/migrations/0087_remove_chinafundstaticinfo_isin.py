# Generated by Django 2.2.7 on 2019-12-27 19:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0086_auto_20191227_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chinafundstaticinfo',
            name='isin',
        ),
    ]
