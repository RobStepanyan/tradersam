# Generated by Django 2.2.7 on 2019-12-13 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0036_ukindexstaticinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='HKIndexStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=4)),
                ('long_name', models.CharField(max_length=75)),
                ('country', models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='HK', max_length=3)),
                ('market', models.CharField(choices=[('HKG', 'The Stock Exchange of Hong Kong Limited')], default='HKG', max_length=3)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='HKD', max_length=3)),
            ],
            options={
                'verbose_name': 'Hong Kong Indices Static Info',
                'verbose_name_plural': 'Hong Kong Indices Static Info',
            },
        ),
        migrations.AlterField(
            model_name='hkstockstaticinfo',
            name='market',
            field=models.CharField(choices=[('HKG', 'The Stock Exchange of Hong Kong Limited')], default='HKG', max_length=3),
        ),
        migrations.AlterField(
            model_name='ukindexstaticinfo',
            name='long_name',
            field=models.CharField(max_length=49),
        ),
    ]
