# Generated by Django 3.1.7 on 2021-03-07 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sheets', '0008_auto_20210307_2339'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playlist',
            old_name='playlist_title',
            new_name='playlist_name',
        ),
    ]