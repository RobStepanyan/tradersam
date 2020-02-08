# Generated by Django 3.0.2 on 2020-01-28 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0106_auto_20200125_1224'),
    ]

    operations = [
        migrations.CreateModel(
            name='AllAssetsAfterLive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('cmdty', 'Commodity'), ('crncy', 'Currency'), ('crptcrncy', 'Cryptocurrency'), ('stck', 'Stock'), ('indx', 'Index'), ('etf', 'ETF'), ('bnd', 'Bond'), ('fnd', 'Fund')], max_length=9)),
                ('short_name', models.CharField(max_length=16)),
                ('link', models.URLField()),
                ('date', models.DateField(default=None, null=True)),
                ('one_year_rng', models.CharField(max_length=30)),
                ('one_year_chg', models.CharField(max_length=12)),
                ('months', models.CharField(max_length=15)),
                ('settlement_day', models.DateField(default=None, null=True)),
                ('last_roll_day', models.DateField(default=None, null=True)),
            ],
            options={
                'verbose_name': '(After Live) All Assets)',
                'verbose_name_plural': '(After Live) All Assets)',
            },
        ),
        migrations.CreateModel(
            name='AllAssetsBeforeLive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('cmdty', 'Commodity'), ('crncy', 'Currency'), ('crptcrncy', 'Cryptocurrency'), ('stck', 'Stock'), ('indx', 'Index'), ('etf', 'ETF'), ('bnd', 'Bond'), ('fnd', 'Fund')], max_length=9)),
                ('short_name', models.CharField(max_length=16)),
                ('link', models.URLField()),
                ('date', models.DateField(default=None, null=True)),
                ('prev_close', models.CharField(max_length=15, null=True)),
                ('Open', models.CharField(max_length=15, null=True)),
            ],
            options={
                'verbose_name': '(Before Live All Assets)',
                'verbose_name_plural': '(Before Live All Assets)',
            },
        ),
        migrations.CreateModel(
            name='AllAssetsHistorical1D',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('cmdty', 'Commodity'), ('crncy', 'Currency'), ('crptcrncy', 'Cryptocurrency'), ('stck', 'Stock'), ('indx', 'Index'), ('etf', 'ETF'), ('bnd', 'Bond'), ('fnd', 'Fund')], max_length=9)),
                ('short_name', models.CharField(max_length=16)),
                ('link', models.URLField()),
                ('date', models.DateTimeField(default=None, null=True)),
                ('price', models.CharField(default=None, max_length=12, null=True)),
            ],
            options={
                'verbose_name': '(1 Day) All Assets',
                'verbose_name_plural': '(1 Day) All Assets',
            },
        ),
        migrations.CreateModel(
            name='AllAssetsHistorical5D',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('cmdty', 'Commodity'), ('crncy', 'Currency'), ('crptcrncy', 'Cryptocurrency'), ('stck', 'Stock'), ('indx', 'Index'), ('etf', 'ETF'), ('bnd', 'Bond'), ('fnd', 'Fund')], max_length=9)),
                ('short_name', models.CharField(max_length=16)),
                ('link', models.URLField()),
                ('date', models.DateTimeField(default=None, null=True)),
                ('price', models.CharField(default=None, max_length=12, null=True)),
            ],
            options={
                'verbose_name': '(5 Days) All Assets',
                'verbose_name_plural': '(5 Days) All Assets',
            },
        ),
        migrations.CreateModel(
            name='AllAssetsLive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Type', models.CharField(choices=[('cmdty', 'Commodity'), ('crncy', 'Currency'), ('crptcrncy', 'Cryptocurrency'), ('stck', 'Stock'), ('indx', 'Index'), ('etf', 'ETF'), ('bnd', 'Bond'), ('fnd', 'Fund')], max_length=9)),
                ('short_name', models.CharField(max_length=16)),
                ('link', models.URLField()),
                ('month', models.DateField(default=None, null=True)),
                ('last_price', models.CharField(max_length=15, null=True)),
                ('last_price_time', models.CharField(max_length=10, null=True)),
                ('high', models.CharField(max_length=15, null=True)),
                ('low', models.CharField(max_length=15, null=True)),
                ('change', models.CharField(max_length=15, null=True)),
                ('change_perc', models.CharField(max_length=12, null=True)),
            ],
            options={
                'verbose_name': '(Live All) Assets',
                'verbose_name_plural': '(Live) All Assets',
            },
        ),
        migrations.DeleteModel(
            name='CommodityAfterLive',
        ),
        migrations.DeleteModel(
            name='CommodityBeforeLive',
        ),
        migrations.DeleteModel(
            name='CommodityHistorical1D',
        ),
        migrations.DeleteModel(
            name='CommodityHistorical5D',
        ),
        migrations.DeleteModel(
            name='CommodityLive',
        ),
    ]