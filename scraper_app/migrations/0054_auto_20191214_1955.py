# Generated by Django 2.2.7 on 2019-12-14 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0053_auto_20191214_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='x',
            name='co',
            field=models.CharField(choices=[('SPDR', 'SPDR'), ('iShares', 'iShares')], max_length=80),
        ),
    ]
