# Generated by Django 4.2.4 on 2023-08-21 10:09

import about.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryCollection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('is_set', models.BooleanField(default=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryCommittee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('is_current', models.BooleanField(default=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryOverview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='About BITS Pilani Library', max_length=100)),
                ('description', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=about.models.libraryOverviewImagePath)),
                ('is_set', models.BooleanField(default=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryRulesAndRegulation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('is_set', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='LibraryTeam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('is_current', models.BooleanField(default=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Rule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('is_bold', models.BooleanField(default=False)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rules', to='about.libraryrulesandregulation')),
            ],
        ),
        migrations.CreateModel(
            name='LibraryTeamMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=20)),
                ('designation', models.CharField(blank=True, max_length=30)),
                ('is_present', models.BooleanField(default=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to=about.models.libraryTeamMemberImagePath)),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='about.libraryteam')),
            ],
        ),
        migrations.CreateModel(
            name='LibraryCommitteeMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=100)),
                ('mobile_number', models.CharField(blank=True, max_length=20)),
                ('department', models.CharField(blank=True, max_length=30)),
                ('is_present', models.BooleanField(default=True)),
                ('committee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='about.librarycommittee')),
            ],
        ),
        migrations.CreateModel(
            name='LibraryCollectionData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.CharField(max_length=100, unique=True)),
                ('data', models.TextField(blank=True, null=True)),
                ('is_int', models.BooleanField(default=False)),
                ('collection', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='data', to='about.librarycollection')),
            ],
        ),
    ]
