# Generated by Django 4.2.4 on 2023-11-21 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0024_librarytiming'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarytiming',
            name='holiday_reason',
            field=models.TextField(blank=True),
        ),
    ]
