# Generated by Django 2.2.7 on 2019-12-27 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0079_auto_20191227_1101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='australiafundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='canadafundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='chinafundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='germanyfundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='hkfundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='japanfundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='usfundstaticinfo',
            name='category',
            field=models.CharField(max_length=40),
        ),
    ]
