# Generated by Django 2.2.5 on 2019-12-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0012_auto_20191207_0925'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hkstockstaticinfo',
            name='market',
            field=models.CharField(choices=[('HKG', 'The Stock Exchange of Hong Kong Limited')], default='HKG', max_length=20),
        ),
    ]
