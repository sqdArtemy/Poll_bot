# Generated by Django 3.2.9 on 2021-11-01 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0004_auto_20211102_0118'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='name',
            field=models.TextField(default=0, unique=True, verbose_name='Language'),
            preserve_default=False,
        ),
    ]