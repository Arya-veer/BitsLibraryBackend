# Generated by Django 4.2.4 on 2023-11-23 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0032_newarrival_position'),
    ]

    operations = [
        migrations.CreateModel(
            name='DonatedBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donor', models.CharField(max_length=60)),
                ('details', models.TextField(blank=True)),
                ('isbn', models.CharField(blank=True, max_length=60)),
                ('image', models.ImageField(blank=True, null=True, upload_to='donated_book_images')),
            ],
            options={
                'verbose_name': 'Donated Book',
                'verbose_name_plural': 'Donated Books',
            },
        ),
    ]
