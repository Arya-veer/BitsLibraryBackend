# Generated by Django 4.2.4 on 2023-11-15 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('papers', '0005_alter_textbook_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='campus',
            field=models.ForeignKey(default='Pilani', on_delete=django.db.models.deletion.CASCADE, related_name='courses', to='databases.campus'),
        ),
    ]
