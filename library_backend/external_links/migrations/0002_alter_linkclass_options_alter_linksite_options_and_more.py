# Generated by Django 4.2.4 on 2023-10-17 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('external_links', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='linkclass',
            options={'verbose_name': 'Link Class', 'verbose_name_plural': 'Link Classes'},
        ),
        migrations.AlterModelOptions(
            name='linksite',
            options={'verbose_name': 'Link Site', 'verbose_name_plural': 'Link Sites'},
        ),
        migrations.AddField(
            model_name='linksite',
            name='url',
            field=models.URLField(default='Url'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='LinkURL',
        ),
    ]
