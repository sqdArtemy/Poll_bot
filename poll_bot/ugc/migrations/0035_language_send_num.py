# Generated by Django 3.2.9 on 2021-11-06 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0034_alter_rightanswers_send_money'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='send_num',
            field=models.TextField(default=0, verbose_name='Send number'),
            preserve_default=False,
        ),
    ]
