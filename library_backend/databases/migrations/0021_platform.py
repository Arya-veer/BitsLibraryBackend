# Generated by Django 4.2.4 on 2023-10-28 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0020_remove_ebook_description'),
    ]

    operations = [
        migrations.CreateModel(
            name='Platform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60)),
                ('link', models.URLField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='platform_images')),
            ],
            options={
                'verbose_name': 'Platform',
                'verbose_name_plural': 'Platforms',
            },
        ),
    ]
