# Generated by Django 4.2.4 on 2023-11-07 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_links', '0009_alter_linksite_link_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linksite',
            name='site_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
