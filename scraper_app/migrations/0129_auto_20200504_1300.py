# Generated by Django 3.0.3 on 2020-05-04 09:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0128_auto_20200503_0502'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='allassetshistorical1d',
            options={'ordering': ['date'], 'verbose_name': '(Historical 1 Day) All Assets', 'verbose_name_plural': '(Historical 1 Day) All Assets'},
        ),
        migrations.AlterModelOptions(
            name='allassetshistorical1y',
            options={'ordering': ['date'], 'verbose_name': '(Historical 1 Year) All Assets', 'verbose_name_plural': '(Historical 1 Year) All Assets'},
        ),
        migrations.AlterModelOptions(
            name='allassetshistorical5d',
            options={'ordering': ['date'], 'verbose_name': '(Historical 5 Days) All Assets', 'verbose_name_plural': '(Historical 5 Days) All Assets'},
        ),
        migrations.AlterModelOptions(
            name='allassetshistorical5y',
            options={'ordering': ['date'], 'verbose_name': '(Historical 5 Years) All Assets', 'verbose_name_plural': '(Historical 5 Years) All Assets'},
        ),
        migrations.AlterModelOptions(
            name='allassetshistorical6m1m',
            options={'ordering': ['date'], 'verbose_name': '(Historical 6M-1M) All Assets', 'verbose_name_plural': '(Historical 6M-1M) All Assets'},
        ),
        migrations.AlterModelOptions(
            name='allassetshistoricalmax',
            options={'ordering': ['date'], 'verbose_name': '(Historical Max Years) All Assets', 'verbose_name_plural': '(Historical Max Years) All Assets'},
        ),
        migrations.AlterField(
            model_name='australiaetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='australiafundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='canadaetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='canadafundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='chinaetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='chinafundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='germanyetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='germanyfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='hketfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='hkfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='japanetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='japanfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='uketfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='ukfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='usetfstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
        migrations.AlterField(
            model_name='usfundstaticinfo',
            name='issuer',
            field=models.CharField(choices=[], max_length=100),
        ),
    ]
