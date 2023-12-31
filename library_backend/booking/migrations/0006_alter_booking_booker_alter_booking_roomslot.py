# Generated by Django 4.2.4 on 2023-10-20 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('booking', '0005_alter_facility_options_alter_roomslot_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='booker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booked_rooms', to='users.userprofile'),
        ),
        migrations.AlterField(
            model_name='booking',
            name='roomslot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='booking.roomslot'),
        ),
    ]
