# Generated by Django 4.2.4 on 2023-11-04 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_links', '0007_alter_linksite_file_alter_linksite_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='linksite',
            name='site_type',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
    ]
