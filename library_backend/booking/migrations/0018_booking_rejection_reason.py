# Generated by Django 4.2.4 on 2023-11-24 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0017_rename_cost_per_minute_facility_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='rejection_reason',
            field=models.TextField(blank=True),
        ),
    ]
