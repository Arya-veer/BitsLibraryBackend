# Generated by Django 4.2.4 on 2023-10-30 09:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_freebook_freebookpick'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dt',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
