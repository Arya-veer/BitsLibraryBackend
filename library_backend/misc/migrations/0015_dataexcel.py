# Generated by Django 4.2.4 on 2024-04-22 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('misc', '0014_revalidate_res'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataExcel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excel', models.FileField(upload_to='data_excel/')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('errors', models.JSONField(default=list)),
                ('purpose', models.CharField(blank=True, choices=[('EBooks', 'EBooks'), ('EJournals', 'EJournals'), ('Faculty', 'Faculty')], max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Data Excel',
                'verbose_name_plural': 'Data Excels',
            },
        ),
    ]
