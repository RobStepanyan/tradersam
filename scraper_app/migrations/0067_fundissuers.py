# Generated by Django 2.2.7 on 2019-12-26 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0066_auto_20191216_1746'),
    ]

    operations = [
        migrations.CreateModel(
            name='FundIssuers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=45)),
                ('country', models.CharField(choices=[('G', 'Global'), ('US', 'United States of America'), ('UK', 'United Kingdom'), ('JP', 'Japan'), ('HK', 'Hong Kong'), ('CH', 'China'), ('CA', 'Canada'), ('GE', 'Germany'), ('AU', 'Australia')], max_length=2)),
            ],
            options={
                'verbose_name': 'Fund Issuers',
                'verbose_name_plural': 'Fund Issuers',
            },
        ),
    ]
