# Generated by Django 4.2.4 on 2023-10-29 07:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0021_platform'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elearning',
            old_name='name',
            new_name='site_name',
        ),
    ]
