# Generated by Django 3.2.13 on 2022-06-28 18:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0018_auto_20220223_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='method',
            name='end_point',
        ),
    ]