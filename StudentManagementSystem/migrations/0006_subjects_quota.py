# Generated by Django 4.1.5 on 2023-01-24 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('StudentManagementSystem', '0005_subjectregistration_remove_students_course_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjects',
            name='quota',
            field=models.FloatField(default=10),
        ),
    ]
