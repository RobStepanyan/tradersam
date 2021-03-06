# Generated by Django 2.2.7 on 2019-12-14 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0047_auto_20191214_0840'),
    ]

    operations = [
        migrations.CreateModel(
            name='GermanyIndexStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=12)),
                ('long_name', models.CharField(max_length=45)),
                ('country', models.CharField(choices=[('G', 'Global'), ('USA', 'United States of America'), ('UK', 'United Kingdom'), ('JPN', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='GE', max_length=3)),
                ('market', models.CharField(choices=[('Frankfurt', 'Frankfurt Stock Exchange (XFRA)'), ('Berlin', 'Berlin Stock Exchange (XBER)'), ('Xetra', 'Xetra Stock Exchange (XETR)'), ('Munich', 'Munich Stock Exchange (XMUN)'), ('Stuttgart', 'Stuttgart Stock Exchange (XSTU)'), ('Dusseldorf', 'Dusseldorf Stock Exchange(XDUS)'), ('Hamburg', 'Hamburg Stock Exchange(XHAM)'), ('Hannover', 'Hannover Stock Exchange (XHAN)')], max_length=10)),
                ('link', models.URLField()),
                ('currency', models.CharField(choices=[('USD', 'US Dollar'), ('JPY', 'Japanese Yen'), ('GBP', 'Pound Sterling'), ('HKD', 'Hong Kong Dollar'), ('CNY', 'Chinese Yuan'), ('CAD', 'Canadian Dollar'), ('EUR', 'Euro'), ('AUD', 'Australian Dollar')], default='EUR', max_length=3)),
            ],
            options={
                'verbose_name': 'Germany Indices Static Info',
                'verbose_name_plural': 'Germany Indices Static Info',
            },
        ),
        migrations.AlterField(
            model_name='canadaindexstaticinfo',
            name='market',
            field=models.CharField(choices=[('NEO', 'Aequitas Neo Exchange (NEO)'), ('Toronto', 'Toronto Stock Exchange (TSX)'), ('CSE', 'Canadian Securities Exchange (CSE)'), ('NASDAQ', 'NASDAQ Canada'), ('TSXV', 'TSX Venture Exchange (TSXV)')], max_length=7),
        ),
        migrations.AlterField(
            model_name='canadastockstaticinfo',
            name='market',
            field=models.CharField(choices=[('NEO', 'Aequitas Neo Exchange (NEO)'), ('Toronto', 'Toronto Stock Exchange (TSX)'), ('CSE', 'Canadian Securities Exchange (CSE)'), ('NASDAQ', 'NASDAQ Canada'), ('TSXV', 'TSX Venture Exchange (TSXV)')], max_length=7),
        ),
    ]
