# Generated by Django 5.1.3 on 2024-12-15 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0003_remove_visit_last_entry_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='interaction_duration',
            field=models.IntegerField(default=0),
        ),
    ]
