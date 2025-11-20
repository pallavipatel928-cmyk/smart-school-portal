"""
API URL Configuration for School App

Defines REST API endpoints using Django REST Framework routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserViewSet, StudentViewSet, TeacherViewSet,
    ClassRoomViewSet, SubjectViewSet, AttendanceViewSet,
    NoticeViewSet, AssignmentViewSet, SubmissionViewSet,
    ResultViewSet
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'classrooms', ClassRoomViewSet, basename='classroom')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'attendance', AttendanceViewSet, basename='attendance')
router.register(r'notices', NoticeViewSet, basename='notice')
router.register(r'assignments', AssignmentViewSet, basename='assignment')
router.register(r'submissions', SubmissionViewSet, basename='submission')
router.register(r'results', ResultViewSet, basename='result')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]
