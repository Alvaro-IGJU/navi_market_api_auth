# Generated by Django 5.1.3 on 2024-12-14 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_remove_event_virtual_location'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='image',
            field=models.TextField(blank=True, null=True),
        ),
    ]
