# Generated by Django 4.2.4 on 2023-11-23 13:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0027_libraryteammember_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Images/LibraryGallery')),
                ('is_set', models.BooleanField(default=True)),
                ('uploaded_on', models.DateField(default=django.utils.timezone.now)),
                ('caption', models.TextField(blank=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
