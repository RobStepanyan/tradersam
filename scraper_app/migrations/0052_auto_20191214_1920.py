# Generated by Django 2.2.7 on 2019-12-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0051_auto_20191214_1208'),
    ]

    operations = [
        migrations.CreateModel(
            name='ETFIssuers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], max_length=2)),
            ],
            options={
                'verbose_name': 'ETF Issuers',
                'verbose_name_plural': 'ETF Issuers',
            },
        ),
        migrations.AlterField(
            model_name='australiaindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='AU', max_length=2),
        ),
        migrations.AlterField(
            model_name='australiastockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='AU', max_length=2),
        ),
        migrations.AlterField(
            model_name='canadaindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CA', max_length=2),
        ),
        migrations.AlterField(
            model_name='canadastockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CA', max_length=2),
        ),
        migrations.AlterField(
            model_name='chinaindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CH', max_length=2),
        ),
        migrations.AlterField(
            model_name='chinastockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='CH', max_length=2),
        ),
        migrations.AlterField(
            model_name='commoditystaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], max_length=2),
        ),
        migrations.AlterField(
            model_name='germanyindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='GE', max_length=2),
        ),
        migrations.AlterField(
            model_name='germanystockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='GE', max_length=2),
        ),
        migrations.AlterField(
            model_name='hkindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='HK', max_length=2),
        ),
        migrations.AlterField(
            model_name='hkstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='HK', max_length=2),
        ),
        migrations.AlterField(
            model_name='japanindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='JP', max_length=2),
        ),
        migrations.AlterField(
            model_name='japanstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='JP', max_length=2),
        ),
        migrations.AlterField(
            model_name='ukindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='UK', max_length=2),
        ),
        migrations.AlterField(
            model_name='ukstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='UK', max_length=2),
        ),
        migrations.AlterField(
            model_name='usindexstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='US', max_length=2),
        ),
        migrations.AlterField(
            model_name='usstockstaticinfo',
            name='country',
            field=models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], default='US', max_length=2),
        ),
    ]
