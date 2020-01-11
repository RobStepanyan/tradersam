# Generated by Django 2.2.7 on 2019-12-27 19:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0085_auto_20191227_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='australiafundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='canadafundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='chinafundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='germanyfundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='hkfundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='japanfundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='ukfundstaticinfo',
            name='inception_date',
            field=models.DateField(default=datetime.date.today, null=True),
        ),
    ]