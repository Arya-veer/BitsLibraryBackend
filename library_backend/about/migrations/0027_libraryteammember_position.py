# Generated by Django 4.2.4 on 2023-11-22 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0026_remove_librarytiming_is_open'),
    ]

    operations = [
        migrations.AddField(
            model_name='libraryteammember',
            name='position',
            field=models.IntegerField(default=1),
        ),
    ]
