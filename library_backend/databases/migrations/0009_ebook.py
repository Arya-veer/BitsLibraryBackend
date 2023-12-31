# Generated by Django 4.2.4 on 2023-10-24 06:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0008_delete_ebook'),
    ]

    operations = [
        migrations.CreateModel(
            name='EBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=160)),
                ('author', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(blank=True, null=True)),
                ('extra_data', models.JSONField(blank=True, default=dict, null=True)),
                ('publisher', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='databases.publisher')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='books', to='databases.subject')),
            ],
            options={
                'verbose_name': 'E-Book',
                'verbose_name_plural': 'E-Books',
            },
        ),
    ]
