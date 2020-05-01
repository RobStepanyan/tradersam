# Generated by Django 3.0.3 on 2020-04-29 18:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users_app', '0004_delete_watchlist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watchlist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('username', models.CharField(max_length=250)),
                ('asset_links', django.contrib.postgres.fields.ArrayField(base_field=models.URLField(), blank=True, size=100)),
            ],
        ),
    ]