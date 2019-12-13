# Generated by Django 2.2.7 on 2019-12-13 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0043_auto_20191213_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='CanadaIndexStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=6)),
                ('long_name', models.CharField(max_length=51)),
                ('country', models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CA', max_length=3)),
                ('market', models.CharField(choices=[('NEO', 'Aequitas Neo Exchange (NEO)'), ('Toronto', 'Toronto Stock Exchange (TSX)'), ('CSE', 'Canadian Securities Exchange (CSE)'), ('NASDAQ', 'NASDAQ Canada')], max_length=7)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='CAD', max_length=3)),
            ],
            options={
                'verbose_name': 'Canada Indices Static Info',
                'verbose_name_plural': 'Canada Indices Static Info',
            },
        ),
    ]
