# Generated by Django 5.1.3 on 2024-12-11 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_position_sector_remove_user_company_sector_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.TextField(blank=True, null=True),
        ),
    ]
