# Generated by Django 2.2.7 on 2019-12-13 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0029_usindexstaticinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usindexstaticinfo',
            name='isin',
        ),
    ]
