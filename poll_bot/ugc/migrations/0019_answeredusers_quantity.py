# Generated by Django 3.2.9 on 2021-11-04 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0018_auto_20211104_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='answeredusers',
            name='quantity',
            field=models.PositiveIntegerField(default=0, verbose_name='Users answered this'),
        ),
    ]
