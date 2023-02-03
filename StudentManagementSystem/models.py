from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Overriding the Default Django Auth
# User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    TEACHER = '1'
    STUDENT = '2'

    user_type_data = ((TEACHER, "Teacher"), (STUDENT, "Student"))
    user_type = models.CharField(default=2, choices=user_type_data, max_length=10)


class Courses(models.Model):
    # id field is auto generated and auto incremented by one using AutoField func
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)

    # need to give default course
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    quota = models.FloatField(default=10)
    objects = models.Manager()


class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE, default=1)
    grade = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class SubjectRegistration(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    member1 = models.IntegerField(blank=False, null=False)
    member2 = models.IntegerField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_message_at = models.DateTimeField(blank=True, null=True)
    objects = models.Manager()


class ChatMessage(models.Model):
    id = models.AutoField(primary_key=True)
    conversation_id = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    from_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    to_id = models.IntegerField(blank=False, null=False)
    text = models.CharField(default="", max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

