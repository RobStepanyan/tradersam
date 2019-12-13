# Generated by Django 2.2.7 on 2019-12-13 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0030_remove_usindexstaticinfo_isin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usindexstaticinfo',
            name='market',
            field=models.CharField(choices=[('NYSE', 'New York Stock Exchange'), ('NASDAQ', 'NASDAQ Stock Market'), ('OTC Markets', 'Over-The-Counter Markets')], max_length=6),
        ),
    ]