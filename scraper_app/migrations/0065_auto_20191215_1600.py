# Generated by Django 2.2.7 on 2019-12-15 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0064_auto_20191215_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='australiaetfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=61),
        ),
        migrations.AlterField(
            model_name='canadaetfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=74),
        ),
        migrations.AlterField(
            model_name='chinaetfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=51),
        ),
        migrations.AlterField(
            model_name='germanyetfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=84),
        ),
        migrations.AlterField(
            model_name='hketfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=79),
        ),
        migrations.AlterField(
            model_name='japanetfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=75),
        ),
        migrations.AlterField(
            model_name='uketfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=84),
        ),
        migrations.AlterField(
            model_name='usetfstaticinfo',
            name='long_name',
            field=models.CharField(max_length=98),
        ),
    ]
