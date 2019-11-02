# Generated by Django 2.2.6 on 2019-10-29 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0030_auto_20191029_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='readinglistitem',
            name='archived',
            field=models.BooleanField(default=False, null=True, verbose_name='Archived'),
        ),
        migrations.AlterField(
            model_name='readinglistitem',
            name='delivered',
            field=models.BooleanField(default=False, null=True, verbose_name='Delivered'),
        ),
        migrations.AlterField(
            model_name='readinglistitem',
            name='trashed',
            field=models.BooleanField(default=False, null=True, verbose_name='Trashed'),
        ),
    ]
