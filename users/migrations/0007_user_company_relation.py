# Generated by Django 5.1.3 on 2024-12-12 19:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('users', '0006_alter_user_managers_user_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='company_relation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='users', to='companies.company'),
        ),
    ]
