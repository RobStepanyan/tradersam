# Generated by Django 2.2.7 on 2019-12-07 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0011_auto_20191207_1244'),
    ]

    operations = [
        migrations.CreateModel(
            name='HKStockStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=60)),
                ('country', models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='HK', max_length=3)),
                ('market', models.CharField(choices=[('HKG', 'The Stock Exchange of Hong Kong Limited')], max_length=20)),
                ('isin', models.CharField(max_length=12)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar')], default='HKD', max_length=3)),
            ],
            options={
                'verbose_name': 'Hong Kong Stocks Static Info',
                'verbose_name_plural': 'Hong Kong Stocks Static Info',
            },
        ),
        migrations.AlterModelOptions(
            name='ukstockstaticinfo',
            options={'verbose_name': 'United Kingdom Stocks Static Info', 'verbose_name_plural': 'United Kingdom Stocks Static Info'},
        ),
        migrations.AlterModelOptions(
            name='usstockstaticinfo',
            options={'verbose_name': 'United States Stocks Static Info', 'verbose_name_plural': 'United States Stocks Static Info'},
        ),
        migrations.AlterField(
            model_name='commoditystaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], max_length=3),
        ),
        migrations.AlterField(
            model_name='japanstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='JPN', max_length=3),
        ),
        migrations.AlterField(
            model_name='japanstockstaticinfo',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar')], default='JPY', max_length=3),
        ),
        migrations.AlterField(
            model_name='ukstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='UK', max_length=3),
        ),
        migrations.AlterField(
            model_name='ukstockstaticinfo',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar')], default='GBP', max_length=3),
        ),
        migrations.AlterField(
            model_name='ukstockstaticinfo',
            name='market',
            field=models.CharField(choices=[('London', 'London Stock Exchange')], default='London', max_length=20),
        ),
        migrations.AlterField(
            model_name='usstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='USA', max_length=3),
        ),
        migrations.AlterField(
            model_name='usstockstaticinfo',
            name='currency',
            field=models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar')], default='USD', max_length=3),
        ),
    ]
