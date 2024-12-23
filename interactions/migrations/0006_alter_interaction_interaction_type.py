# Generated by Django 5.1.3 on 2024-12-23 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interactions', '0005_remove_interaction_interaction_details'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interaction',
            name='interaction_type',
            field=models.CharField(choices=[('mailbox', 'Mailbox'), ('info_pc', 'Info PC'), ('play_video', 'Play Video'), ('download_catalog', 'Download Catalog'), ('schedule_meeting', 'Schedule Meeting'), ('talk_chatbot', 'Talk Chatbot')], max_length=50),
        ),
    ]
