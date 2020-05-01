# Generated by Django 3.0.3 on 2020-04-29 18:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0126_merge_20200426_1049'),
    ]

    operations = [
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