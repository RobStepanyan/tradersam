# Generated by Django 3.0.3 on 2020-02-28 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0115_auto_20200228_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='allassetsafterlive',
            name='short_name',
        ),
        migrations.RemoveField(
            model_name='allassetshistorical1d',
            name='short_name',
        ),
        migrations.RemoveField(
            model_name='allassetslive',
            name='short_name',
        ),
        migrations.AddField(
            model_name='allassetslive',
            name='time',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]