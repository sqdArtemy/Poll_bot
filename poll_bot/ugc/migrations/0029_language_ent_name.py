# Generated by Django 3.2.9 on 2021-11-05 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0028_profile_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='language',
            name='ent_name',
            field=models.TextField(default=0, verbose_name='Enter yout name'),
            preserve_default=False,
        ),
    ]