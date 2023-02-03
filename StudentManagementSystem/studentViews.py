from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.db.models import Q

from .models import CustomUser, Courses, Subjects, StudentResult, SubjectRegistration


def student_home(request):
    student = CustomUser.objects.get(id=request.user.id)
    if student.user_type == "2":
        registered_courses = SubjectRegistration.objects.filter(student_id=student)
        context = {

            "student_name": student.first_name,
            "student_lastname": student.last_name,
            "registered_courses": registered_courses
        }
        return render(request, "student_home.html", context)
    else:
        return render(request, 'login.html')


def results(request):
    student = CustomUser.objects.get(id=request.user.id)
    if student.user_type == "2":
        student_result = StudentResult.objects.raw('SELECT * FROM StudentManagementSystem_studentresult WHERE student_id_id = %s', [request.user.id])
        context = {
            "student_result": student_result,
        }
        return render(request, "view_results.html", context)
    else:
        return render(request, 'login.html')


def subject_registration(request):
    student = CustomUser.objects.get(id=request.user.id)
    if student.user_type == "2":
        subjects = Subjects.objects.raw('SELECT * FROM StudentManagementSystem_subjects')
        registered_subjects = SubjectRegistration.objects.filter(student_id=student)
        context = {
            "subjects": subjects,
            "registered_subjects": registered_subjects
        }
        return render(request, "subject_registration.html", context)
    else:
        return render(request, 'login.html')


@csrf_exempt
def register_to_subject(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('subject_registration')
    else:
        subject_id = request.POST.get('subject')
        # Get subject quota to check later
        subject_quota = Subjects.objects.get(id=subject_id).quota
        # Django's Q module used to combine multiple conditions with AND or OR statements
        C1 = Q(subject_id=subject_id)
        C2 = Q(student_id=request.user.id)
        if SubjectRegistration.objects.filter(C1 & C2).exists():
            messages.error(request, "This student already registered to this subject!")
            return redirect('subject_registration')
        elif SubjectRegistration.objects.filter(subject_id=subject_id).count() >= subject_quota:
            messages.error(request, "Max number of students have been reached for this subject!")
            return redirect('subject_registration')
        else:
            try:
                student = CustomUser.objects.get(id=request.user.id)
                subject = Subjects.objects.get(id=subject_id)
                subject_registration = SubjectRegistration(student_id=student, subject_id=subject)
                subject_registration.save()
                messages.success(request, "Registration Added Successfully!")
                return redirect('subject_registration')
            except Exception as e:
                print(e)
                messages.error(request, "Failed to Register to Subject!")
                return redirect('subject_registration')


@csrf_exempt
def unregister_subject(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method")
        return redirect('subject_registration')
    else:
        subject_id = request.POST.get('subject_to_unregister')
        # Django's Q module used to combine multiple conditions with AND or OR statements
        C1 = Q(subject_id=subject_id)
        C2 = Q(student_id=request.user.id)
        if SubjectRegistration.objects.filter(C1 & C2).exists():
            SubjectRegistration.objects.filter(C1 & C2).delete()
            messages.success(request, "Subject dropped successfully")
            return redirect('subject_registration')
        else:
            messages.error(request, "Something went horribly wrong :(")
            return redirect('subject_registration')

