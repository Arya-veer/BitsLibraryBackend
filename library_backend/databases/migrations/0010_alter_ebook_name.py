# Generated by Django 4.2.4 on 2023-10-24 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0009_ebook'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ebook',
            name='name',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
