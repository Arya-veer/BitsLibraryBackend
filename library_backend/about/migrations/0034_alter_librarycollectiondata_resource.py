# Generated by Django 4.2.4 on 2024-03-22 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0033_remove_librarycollection_is_set_bookmarquee_campus_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='librarycollectiondata',
            name='resource',
            field=models.CharField(max_length=100),
        ),
    ]
