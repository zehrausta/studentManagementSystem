# Generated by Django 4.1.5 on 2023-01-24 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentManagementSystem', '0007_conversation_chatmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conversation',
            name='last_message_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
