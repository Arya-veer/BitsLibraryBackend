# Generated by Django 4.2.4 on 2023-11-23 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0037_alter_donatedbook_book_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='donatedbook',
            options={'verbose_name': 'Donated Book or BITSian Authored Book', 'verbose_name_plural': 'Donated Books BITSian or Authored Books'},
        ),
    ]
