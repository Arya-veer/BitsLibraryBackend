# Generated by Django 4.2.4 on 2023-09-07 06:14

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='condition',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='room',
            name='slots',
        ),
        migrations.AlterField(
            model_name='room',
            name='capacity',
            field=models.IntegerField(null=True, verbose_name='Room Capacity'),
        ),
        migrations.AlterField(
            model_name='room',
            name='name',
            field=models.CharField(blank=True, max_length=60, verbose_name='Room Name'),
        ),
        migrations.CreateModel(
            name='Slots',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slots', models.DurationField(default=datetime.timedelta(seconds=3600), verbose_name='')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='booking.room')),
            ],
        ),
    ]
