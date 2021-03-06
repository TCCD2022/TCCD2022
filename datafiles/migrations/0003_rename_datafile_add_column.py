# Generated by Django 3.2.9 on 2021-11-11 11:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('datafiles', '0002_datamodel_userid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='datamodel',
            old_name='userid',
            new_name='user',
        ),
        migrations.RenameModel(
            old_name='DataModel',
            new_name='Datafile',
        ),
        migrations.CreateModel(
            name='Column',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('type', models.CharField(choices=[('NM', 'Number'), ('ST', 'String')], max_length=2)),
                ('scale', models.CharField(choices=[('CT', 'Continuous'), ('OD', 'Ordinal'), ('NM', 'Nominal')], max_length=2, null=True)),
                ('datafile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='datafiles.datafile')),
            ],
        ),
    ]
