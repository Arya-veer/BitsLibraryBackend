# Generated by Django 4.2.4 on 2024-05-07 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_alter_userprofile_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='FootageRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request', models.TextField()),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Closed', 'Closed')], default='Pending', max_length=200)),
                ('remarks', models.TextField(blank=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='footage_requests', to='users.userprofile')),
            ],
            options={
                'verbose_name': 'CCTV Footage Request',
                'verbose_name_plural': 'CCTV Footage Requests',
            },
        ),
    ]
