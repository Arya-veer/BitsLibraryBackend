# Generated by Django 4.2.4 on 2023-10-27 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0006_remove_feedback_email_remove_feedback_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='designation',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='feedbacks/'),
        ),
    ]
