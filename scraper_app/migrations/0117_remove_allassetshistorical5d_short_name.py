# Generated by Django 3.0.3 on 2020-02-28 18:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0116_auto_20200228_2149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allassetshistorical5d',
            name='short_name',
        ),
    ]
