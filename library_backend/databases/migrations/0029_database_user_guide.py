# Generated by Django 4.2.4 on 2023-11-16 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0028_newarrival'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='user_guide',
            field=models.FileField(blank=True, null=True, upload_to='database_user_guides'),
        ),
    ]
