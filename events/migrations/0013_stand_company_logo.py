# Generated by Django 5.1.3 on 2025-01-19 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0012_stand_url_web'),
    ]

    operations = [
        migrations.AddField(
            model_name='stand',
            name='company_logo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
