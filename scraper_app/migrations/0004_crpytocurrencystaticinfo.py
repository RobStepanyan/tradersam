# Generated by Django 2.2.5 on 2019-12-02 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0003_currencystaticinfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrpytoCurrencyStaticInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=10)),
                ('long_name', models.CharField(max_length=30)),
                ('link', models.URLField()),
            ],
        ),
    ]
