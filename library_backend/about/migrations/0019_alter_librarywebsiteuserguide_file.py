# Generated by Django 4.2.4 on 2023-11-18 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0018_librarywebsiteuserguide'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarywebsiteuserguide',
            name='file',
            field=models.FileField(max_length=200, upload_to='user_guide'),
        ),
    ]
