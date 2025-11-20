"""
REST API Views for Smart School Management Portal

Provides REST API endpoints for all models.
"""

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from .models import (
    User, Student, Teacher, ClassRoom, Subject,
    Attendance, Notice, Assignment, Submission, Result
)
from .serializers import (
    UserSerializer, StudentSerializer, TeacherSerializer,
    ClassRoomSerializer, SubjectSerializer, AttendanceSerializer,
    NoticeSerializer, AssignmentSerializer, SubmissionSerializer,
    ResultSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """API endpoint for users"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ModelViewSet):
    """API endpoint for students"""
    queryset = Student.objects.select_related('user', 'classroom').all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def attendance(self, request, pk=None):
        """Get attendance records for a student"""
        student = self.get_object()
        attendances = Attendance.objects.filter(student=student)
        serializer = AttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        """Get exam results for a student"""
        student = self.get_object()
        results = Result.objects.filter(student=student)
        serializer = ResultSerializer(results, many=True)
        return Response(serializer.data)


class TeacherViewSet(viewsets.ModelViewSet):
    """API endpoint for teachers"""
    queryset = Teacher.objects.select_related('user').prefetch_related('subjects').all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassRoomViewSet(viewsets.ModelViewSet):
    """API endpoint for classrooms"""
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students in a classroom"""
        classroom = self.get_object()
        students = Student.objects.filter(classroom=classroom)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class SubjectViewSet(viewsets.ModelViewSet):
    """API endpoint for subjects"""
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class AttendanceViewSet(viewsets.ModelViewSet):
    """API endpoint for attendance"""
    queryset = Attendance.objects.select_related('student', 'subject', 'marked_by').all()
    serializer_class = AttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter attendance based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'student':
            try:
                student = user.student_profile
                queryset = queryset.filter(student=student)
            except Student.DoesNotExist:
                queryset = queryset.none()
        
        return queryset


class NoticeViewSet(viewsets.ModelViewSet):
    """API endpoint for notices"""
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter notices based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        queryset = queryset.filter(
            Q(target_role='all') | Q(target_role=user.role),
            is_active=True
        )
        
        return queryset


class AssignmentViewSet(viewsets.ModelViewSet):
    """API endpoint for assignments"""
    queryset = Assignment.objects.select_related('subject', 'classroom', 'uploaded_by').all()
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter assignments based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'student':
            try:
                student = user.student_profile
                queryset = queryset.filter(classroom=student.classroom)
            except Student.DoesNotExist:
                queryset = queryset.none()
        elif user.role == 'teacher':
            try:
                teacher = user.teacher_profile
                queryset = queryset.filter(uploaded_by=teacher)
            except Teacher.DoesNotExist:
                queryset = queryset.none()
        
        return queryset
    
    @action(detail=True, methods=['get'])
    def submissions(self, request, pk=None):
        """Get all submissions for an assignment"""
        assignment = self.get_object()
        submissions = Submission.objects.filter(assignment=assignment)
        serializer = SubmissionSerializer(submissions, many=True)
        return Response(serializer.data)


class SubmissionViewSet(viewsets.ModelViewSet):
    """API endpoint for submissions"""
    queryset = Submission.objects.select_related('assignment', 'student', 'graded_by').all()
    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter submissions based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'student':
            try:
                student = user.student_profile
                queryset = queryset.filter(student=student)
            except Student.DoesNotExist:
                queryset = queryset.none()
        
        return queryset


class ResultViewSet(viewsets.ModelViewSet):
    """API endpoint for results"""
    queryset = Result.objects.select_related('student', 'subject').all()
    serializer_class = ResultSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Filter results based on user role"""
        queryset = super().get_queryset()
        user = self.request.user
        
        if user.role == 'student':
            try:
                student = user.student_profile
                queryset = queryset.filter(student=student)
            except Student.DoesNotExist:
                queryset = queryset.none()
        
        return queryset
