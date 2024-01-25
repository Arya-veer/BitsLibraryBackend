# Generated by Django 4.2.4 on 2023-11-15 08:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0028_newarrival'),
        ('papers', '0006_bitscampus_course_campus'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='campus',
            field=models.ForeignKey(default='Pilani', on_delete=django.db.models.deletion.CASCADE, related_name='papers', to='databases.campus'),
        ),
    ]
