# Generated by Django 4.2.4 on 2023-10-29 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0023_elearning_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='elearning',
            old_name='link',
            new_name='url',
        ),
    ]
