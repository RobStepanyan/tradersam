# Generated by Django 2.2.7 on 2019-12-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0024_auto_20191210_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='germanystockstaticinfo',
            name='long_name',
            field=models.CharField(max_length=45),
        ),
    ]
