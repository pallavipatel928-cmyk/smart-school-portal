"""
REST API Serializers for Smart School Management Portal

Converts model instances to JSON and vice versa.
"""

from rest_framework import serializers
from .models import (
    User, Student, Teacher, ClassRoom, Subject,
    Attendance, Notice, Assignment, Submission, Result
)


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone', 'date_of_birth']
        read_only_fields = ['id']


class ClassRoomSerializer(serializers.ModelSerializer):
    """Serializer for ClassRoom model"""
    class Meta:
        model = ClassRoom
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    """Serializer for Subject model"""
    class Meta:
        model = Subject
        fields = '__all__'


class TeacherSerializer(serializers.ModelSerializer):
    """Serializer for Teacher model"""
    user = UserSerializer(read_only=True)
    subjects = SubjectSerializer(many=True, read_only=True)
    
    class Meta:
        model = Teacher
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    """Serializer for Student model"""
    user = UserSerializer(read_only=True)
    classroom = ClassRoomSerializer(read_only=True)
    
    class Meta:
        model = Student
        fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    marked_by = TeacherSerializer(read_only=True)
    
    class Meta:
        model = Attendance
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    """Serializer for Notice model"""
    created_by = UserSerializer(read_only=True)
    
    class Meta:
        model = Notice
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    """Serializer for Assignment model"""
    subject = SubjectSerializer(read_only=True)
    classroom = ClassRoomSerializer(read_only=True)
    uploaded_by = TeacherSerializer(read_only=True)
    
    class Meta:
        model = Assignment
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for Submission model"""
    assignment = AssignmentSerializer(read_only=True)
    student = StudentSerializer(read_only=True)
    graded_by = TeacherSerializer(read_only=True)
    
    class Meta:
        model = Submission
        fields = '__all__'


class ResultSerializer(serializers.ModelSerializer):
    """Serializer for Result model"""
    student = StudentSerializer(read_only=True)
    subject = SubjectSerializer(read_only=True)
    
    class Meta:
        model = Result
        fields = '__all__'
