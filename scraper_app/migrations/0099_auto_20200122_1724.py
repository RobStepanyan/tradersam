# Generated by Django 2.2.7 on 2020-01-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0098_allassetshistorical5y'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commoditystaticinfo',
            name='base_symbol',
            field=models.CharField(max_length=7),
        ),
    ]
