# Generated by Django 4.2.4 on 2023-11-17 10:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0030_rename_user_guide_database_user_guide_file_and_more'),
        ('papers', '0007_paper_campus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paper',
            name='campus',
            field=models.ForeignKey(default='Pilani', on_delete=django.db.models.deletion.PROTECT, related_name='papers', to='databases.campus'),
        ),
        migrations.AlterField(
            model_name='paper',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='papers', to='papers.course'),
        ),
    ]
