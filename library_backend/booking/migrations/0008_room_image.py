# Generated by Django 4.2.4 on 2023-10-23 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0007_alter_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='image',
            field=models.ImageField(null=True, upload_to='room_images'),
        ),
    ]
