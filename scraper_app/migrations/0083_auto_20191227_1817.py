# Generated by Django 2.2.7 on 2019-12-27 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper_app', '0082_auto_20191227_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='australiafundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='canadafundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='chinafundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='germanyfundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='hkfundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='japanfundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='ukfundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='usfundstaticinfo',
            name='category_descrptn',
            field=models.TextField(),
        ),
    ]
