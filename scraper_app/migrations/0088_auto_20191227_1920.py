# Generated by Django 2.2.7 on 2019-12-27 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0087_remove_chinafundstaticinfo_isin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='australiafundstaticinfo',
            name='isin',
        ),
        migrations.RemoveField(
            model_name='canadafundstaticinfo',
            name='isin',
        ),
    ]
