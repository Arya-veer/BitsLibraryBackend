# Generated by Django 4.2.4 on 2023-10-29 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0022_rename_name_elearning_site_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='elearning',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='elearning_images'),
        ),
    ]
