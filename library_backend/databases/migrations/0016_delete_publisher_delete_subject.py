# Generated by Django 4.2.4 on 2023-10-24 06:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0015_publisher_alter_subject_name_delete_ebook'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Publisher',
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
