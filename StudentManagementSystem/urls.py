"""StudentManagementSystem URL Configuration

The `urlpatterns` list routes URLs to templates. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function templates
    1. Add an import:  from my_app import templates
    2. Add a URL to urlpatterns:  path('', templates.home, name='home')
Class-based templates
    1. Add an import:  from other_app.templates import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from . import teacherViews, studentViews

urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('login', views.loginUser, name="login"),
    path('logout_user', views.logout_user, name="logout_user"),
    path('registration', views.registration, name="registration"),
    path('doLogin', views.doLogin, name="doLogin"),
    path('doRegistration', views.doRegistration, name="doRegistration"),
    path('conversations/', views.conversations, name="conversations"),
    path('chat/<int:id>', views.chat, name="chat"),
    path('sendMessage', views.sendMessage, name="sendMessage"),

    # URLS for Student
    path('student_home/', studentViews.student_home, name="student_home"),
    path('results/', studentViews.results, name="results"),
    path('subject_registration/', studentViews.subject_registration, name="subject_registration"),
    path('register_to_subject/', studentViews.register_to_subject, name="register_to_subject"),
    path('unregister_subject/', studentViews.unregister_subject, name="unregister_subject"),

    # URLS for Staff
    path('teacher_home/', teacherViews.teacher_home, name="teacher_home"),
    path('add_result/', teacherViews.add_result, name="add_result"),
    path('add_result_save/', teacherViews.add_result_save, name="add_result_save"),
    path('create_subject/', teacherViews.create_subject, name="create_subject"),
    path('submit_create_subject/', teacherViews.submit_create_subject, name="submit_create_subject"),

]
