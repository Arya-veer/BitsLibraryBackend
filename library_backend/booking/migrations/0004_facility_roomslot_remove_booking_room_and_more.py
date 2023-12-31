# Generated by Django 4.2.4 on 2023-10-20 13:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0003_rename_slots_slot'),
    ]

    operations = [
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('name', models.CharField(blank=True, max_length=60, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoomSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name_plural': 'Facilities',
            },
        ),
        migrations.RemoveField(
            model_name='booking',
            name='room',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='slot',
        ),
        migrations.RemoveField(
            model_name='room',
            name='num_slots',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='room',
        ),
        migrations.RemoveField(
            model_name='slot',
            name='slots',
        ),
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='booking',
            name='no_of_participants',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='endtime',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='slot',
            name='starttime',
            field=models.TimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Facilities',
        ),
        migrations.AddField(
            model_name='roomslot',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roomslots', to='booking.room'),
        ),
        migrations.AddField(
            model_name='roomslot',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roomslots', to='booking.slot'),
        ),
        migrations.AddField(
            model_name='booking',
            name='requirements',
            field=models.ManyToManyField(related_name='bookings', to='booking.facility'),
        ),
        migrations.AddField(
            model_name='booking',
            name='roomslot',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='booked_roomslot', to='booking.roomslot'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='available_facilities',
            field=models.ManyToManyField(to='booking.facility'),
        ),
    ]
