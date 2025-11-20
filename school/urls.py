"""
URL Configuration for School App

Maps URLs to view functions.
"""

from django.urls import path
from . import views

urlpatterns = [
    # Home and Authentication
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    
    # Students
    path('students/', views.student_list, name='student_list'),
    path('students/<int:pk>/', views.student_detail, name='student_detail'),
    
    # Teachers
    path('teachers/', views.teacher_list, name='teacher_list'),
    path('teachers/<int:pk>/', views.teacher_detail, name='teacher_detail'),
    
    # Attendance
    path('attendance/', views.attendance_list, name='attendance_list'),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    
    # Notices
    path('notices/', views.notice_list, name='notice_list'),
    path('notices/create/', views.notice_create, name='notice_create'),
    
    # Assignments
    path('assignments/', views.assignment_list, name='assignment_list'),
    path('assignments/create/', views.assignment_create, name='assignment_create'),
    path('assignments/<int:pk>/', views.assignment_detail, name='assignment_detail'),
    path('assignments/<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    
    # Results
    path('results/', views.result_list, name='result_list'),
    path('results/create/', views.result_create, name='result_create'),
    
    # ADVANCED FEATURES URLs
    # Timetable
    path('timetable/', views.timetable_view, name='timetable'),
    
    # Exams
    path('exams/', views.exam_list, name='exam_list'),
    
    # Leave Applications
    path('leave/', views.leave_application_list, name='leave_list'),
    path('leave/apply/', views.apply_leave, name='apply_leave'),
    path('leave/<int:pk>/review/', views.leave_review, name='leave_review'),
    
    # Fee Management
    path('fees/', views.fee_list, name='fee_list'),
    
    # Messaging System
    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>/', views.message_detail, name='message_detail'),
    path('message/send/', views.send_message, name='send_message'),
    
    # Events/Calendar
    path('events/', views.event_calendar, name='events'),
    
    # Library
    path('library/', views.library_books, name='library_books'),
    path('library/my-books/', views.my_borrowed_books, name='my_books'),
    
    # Analytics
    path('analytics/', views.student_analytics, name='student_analytics'),
    
    # Meeting Portal
    path('meetings/', views.meeting_portal, name='meeting_portal'),
    path('meetings/create/', views.meeting_create, name='meeting_create'),
    path('meetings/<int:pk>/', views.meeting_detail, name='meeting_detail'),
]
