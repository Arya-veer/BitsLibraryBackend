# Generated by Django 4.2.4 on 2023-11-08 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0015_bookmarquee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libraryteam',
            name='is_current',
            field=models.BooleanField(default=True),
        ),
    ]
