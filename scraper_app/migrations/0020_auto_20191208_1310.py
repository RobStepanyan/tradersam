# Generated by Django 2.2.7 on 2019-12-08 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0019_auto_20191208_1658'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chinastockstaticinfo',
            name='market',
            field=models.CharField(choices=[('Shanghai', 'Shanghai Stock Exchange'), ('Shenzhen', 'Shenzhen Stock Exchange')], max_length=20),
        ),
        migrations.AlterField(
            model_name='chinastockstaticinfo',
            name='short_name',
            field=models.CharField(max_length=6),
        ),
    ]