# Generated by Django 4.2.4 on 2023-10-30 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_articlebookrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='FreeBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fbn', models.IntegerField()),
                ('title', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('publisher', models.CharField(max_length=200)),
                ('year', models.IntegerField()),
                ('edition', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Free Book',
                'verbose_name_plural': 'Free Books',
            },
        ),
        migrations.CreateModel(
            name='FreeBookPick',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=200)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_book_picks', to='users.freebook')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='free_book_picks', to='users.userprofile')),
            ],
            options={
                'verbose_name': 'Free Book Pick',
                'verbose_name_plural': 'Free Book Picks',
            },
        ),
    ]
