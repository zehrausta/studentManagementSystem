from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

from .models import CustomUser, Subjects, StudentResult, Courses, SubjectRegistration


def teacher_home(request):
    teacher = CustomUser.objects.get(id=request.user.id)
    if teacher.user_type == "1":
        students_count = CustomUser.objects.filter(user_type=2).count()
        # cursor func is used to execute raw sql queries in Django
        cursor = connection.cursor()
        cursor.execute('SELECT COUNT(*) FROM StudentManagementSystem_subjects')
        subject_count = cursor.fetchall()[0][0]
        # subject_count = Subjects.objects.count()

        context = {
            "students_count": students_count,
            "subject_count": subject_count,
        }
        return render(request, "teacher_home.html", context)
    else:
        return render(request, 'login.html')


def add_result(request):
    teacher = CustomUser.objects.get(id=request.user.id)
    if teacher.user_type == "1":
        subjects = Subjects.objects.all()
        students = CustomUser.objects.filter(user_type=2).all()
        context = {
            "subjects": subjects,
            "students": students
        }
        return render(request, "add_result.html", context)
    else:
        return render(request, 'login.html')


@csrf_exempt
def add_result_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('add_result')
    else:
        student_id = request.POST.get('student')
        subject_id = request.POST.get('subject')
        grade = request.POST.get('grade')
        Q1 = Q(subject_id=subject_id)
        Q2 = Q(student_id=student_id)
        if not SubjectRegistration.objects.filter(Q1 & Q2).exists():
            messages.error(request, "This student is not registered for this subject.")
            return redirect('add_result')

        elif StudentResult.objects.filter(Q1 & Q2).exists():
            result = StudentResult.objects.get(Q1 & Q2)
            result.grade = grade
            result.save()
            messages.success(request, "This student already had a grade for this subject! Grade updated with new one.")
            return redirect('add_result')
        else:
            try:
                student = CustomUser.objects.get(id=student_id)
                subject = Subjects.objects.get(id=subject_id)
                result = StudentResult(student_id=student, subject_id=subject, grade=grade)
                result.save()
                messages.success(request, "Result Added Successfully!")
                return redirect('add_result')
            except Exception as e:
                print(e)
                messages.error(request, "Failed to Add Result!")
                return redirect('add_result')


def create_subject(request):
    teacher = CustomUser.objects.get(id=request.user.id)
    if teacher.user_type == "1":
        courses = Courses.objects.all()
        context = {
            "courses": courses
        }
        return render(request, "create_subject.html", context)
    else:
        return render(request, 'login.html')


@csrf_exempt
def submit_create_subject(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('create_subject')
    else:
        course_id = request.POST.get('course')
        subject_name = request.POST.get('subject_name')
        quota = request.POST.get('quota')

        try:
            course = Courses.objects.get(id=course_id)
            subject = Subjects(course_id=course, subject_name=subject_name, quota=quota)
            subject.save()
            messages.success(request, "Subject Added Successfully!")
            return redirect('create_subject')
        except Exception as e:
            print(e)
            messages.error(request, "Failed to Create Subject!")
            return redirect('create_subject')