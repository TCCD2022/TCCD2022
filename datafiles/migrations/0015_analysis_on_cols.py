# Generated by Django 3.2.10 on 2021-12-24 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0014_alter_analysis_results_file_format'),
    ]

    operations = [
        migrations.AddField(
            model_name='analysis',
            name='on_cols',
            field=models.ManyToManyField(through='datafiles.Analysis_on_columns', to='datafiles.Column'),
        ),
    ]