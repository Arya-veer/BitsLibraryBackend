


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0026_database_id_alter_database_name'),
    ]

    operations = [

        migrations.AddField(
                    model_name='database',
                    name='id',
                    field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
                    preserve_default=False,
                ),
    ]