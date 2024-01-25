# Generated by Django 4.2.4 on 2023-11-19 05:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0022_alter_event_title_alter_news_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryCalendar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('imgae', models.ImageField(max_length=200, upload_to='Calendars')),
                ('is_set', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='LibraryTiming',
        ),
    ]
