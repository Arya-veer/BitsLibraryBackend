# Generated by Django 4.2.4 on 2023-09-30 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0004_feedback'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarycollection',
            name='title',
            field=models.CharField(default='Library Collection', max_length=40),
            preserve_default=False,
        ),
    ]
