# Generated by Django 3.1.7 on 2021-03-04 09:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0005_auto_20210304_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sheet',
            old_name='file',
            new_name='chords',
        ),
    ]