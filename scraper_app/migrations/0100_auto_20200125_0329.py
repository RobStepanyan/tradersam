# Generated by Django 3.0.2 on 2020-01-25 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0099_auto_20200122_1724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commoditystaticinfo',
            name='unit',
            field=models.CharField(max_length=15, null=True),
        ),
    ]