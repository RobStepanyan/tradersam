# Generated by Django 2.2.7 on 2019-12-27 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0080_auto_20191227_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='australiafundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='canadafundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='chinafundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='germanyfundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='hkfundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='japanfundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='ukfundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='usfundstaticinfo',
            name='min_investment',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
