# Generated by Django 4.2.4 on 2023-08-21 10:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0002_tabularrules'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TabularRules',
            new_name='TabularRule',
        ),
    ]
