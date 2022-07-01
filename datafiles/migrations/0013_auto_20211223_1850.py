# Generated by Django 3.2.10 on 2021-12-23 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0012_alter_column_col_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='file_format',
            field=models.TextField(choices=[('CSV', 'Comma-separated values'), ('dat', 'dat'), ('gz', 'gz'), ('bz', 'bz2'), ('UNS', 'Unsupported')], max_length=3, null=True),
        ),
        migrations.CreateModel(
            name='Analysis_results',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=2048)),
                ('file_format', models.CharField(max_length=2048)),
                ('analysis_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datafiles.analysis')),
            ],
        ),
        migrations.CreateModel(
            name='Analysis_on_columns',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dependent', models.BooleanField(help_text='Whether the column represents an independent variable.', null=True)),
                ('analysis_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datafiles.analysis')),
                ('column_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datafiles.column')),
            ],
        ),
    ]
