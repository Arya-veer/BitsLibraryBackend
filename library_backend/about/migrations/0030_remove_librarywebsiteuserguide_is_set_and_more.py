# Generated by Django 4.2.4 on 2023-11-25 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('about', '0029_librarycommitteemember_position'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='librarywebsiteuserguide',
            name='is_set',
        ),
        migrations.RemoveField(
            model_name='librarywebsiteuserguide',
            name='uploaded_on',
        ),
        migrations.AddField(
            model_name='librarywebsiteuserguide',
            name='link',
            field=models.URLField(blank=True),
        ),
        migrations.AddField(
            model_name='librarywebsiteuserguide',
            name='title',
            field=models.CharField(default='Website User Guide', max_length=200),
        ),
    ]
