# Generated by Django 5.1.3 on 2025-01-09 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0007_alter_interaction_interaction_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='interaction',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], max_length=10, null=True),
        ),
    ]
