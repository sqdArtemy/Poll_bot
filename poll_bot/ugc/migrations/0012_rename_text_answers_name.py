# Generated by Django 3.2.9 on 2021-11-02 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ugc', '0011_rename_question_question_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answers',
            old_name='text',
            new_name='name',
        ),
    ]