# Generated by Django 3.0.2 on 2020-01-25 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0105_commodityafterlive'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commodityafterlive',
            name='one_year_chg',
            field=models.CharField(max_length=12),
        ),
    ]
