# Generated by Django 2.2.7 on 2019-12-28 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0090_auto_20191228_1518'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='etfissuers',
            options={'verbose_name': '(Other) ETF Issuers', 'verbose_name_plural': '(Other) ETF Issuers'},
        ),
        migrations.AlterModelOptions(
            name='fundissuers',
            options={'verbose_name': '(Other) Fund Issuers', 'verbose_name_plural': '(Other) Fund Issuers'},
        ),
    ]