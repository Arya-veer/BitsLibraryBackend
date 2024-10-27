# Generated by Django 4.0.10 on 2024-09-12 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0041_publication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='blog_images')),
                ('published_date', models.DateField(blank=True, null=True)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Blog',
                'verbose_name_plural': 'Blogs',
            },
        ),
    ]