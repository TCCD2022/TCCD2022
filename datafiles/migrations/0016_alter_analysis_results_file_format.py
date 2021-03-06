# Generated by Django 3.2.10 on 2022-01-21 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datafiles', '0015_analysis_on_cols'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis_results',
            name='file_format',
            field=models.CharField(choices=[('png', 'PNG'), ('pdf', 'pdf'), ('jpg', 'JPG'), ('txt', 'TXT'), ('csv', 'CSV'), ('html', 'HTML')], max_length=4),
        ),
    ]
