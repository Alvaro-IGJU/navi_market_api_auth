# Generated by Django 5.1.3 on 2024-12-19 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0006_event_max_stands'),
    ]

    operations = [
        migrations.AddField(
            model_name='stand',
            name='pdf',
            field=models.TextField(blank=True, null=True),
        ),
    ]
