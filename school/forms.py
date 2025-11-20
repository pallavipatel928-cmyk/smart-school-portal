"""
Forms for Smart School Management Portal

This module contains all forms for user registration, login,
and data entry for various models.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import (
    User, Student, Teacher, ClassRoom, Subject,
    Attendance, Notice, Assignment, Submission, Result
)


# ==================== User Registration Forms ====================
class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration.
    Extends Django's UserCreationForm to include additional fields.
    """
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First Name'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last Name'
    }))
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})


class UserLoginForm(AuthenticationForm):
    """Custom login form with Bootstrap styling"""
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))


# ==================== Student Form ====================
class StudentForm(forms.ModelForm):
    """Form for creating/updating student profiles"""
    
    class Meta:
        model = Student
        fields = ['roll_no', 'classroom', 'parent_name', 'parent_phone', 'admission_date', 'is_active']
        widgets = {
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'parent_name': forms.TextInput(attrs={'class': 'form-control'}),
            'parent_phone': forms.TextInput(attrs={'class': 'form-control'}),
            'admission_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==================== Teacher Form ====================
class TeacherForm(forms.ModelForm):
    """Form for creating/updating teacher profiles"""
    
    class Meta:
        model = Teacher
        fields = ['subjects', 'qualification', 'experience_years', 'joining_date', 'is_active']
        widgets = {
            'subjects': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'qualification': forms.TextInput(attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(attrs={'class': 'form-control'}),
            'joining_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==================== ClassRoom Form ====================
class ClassRoomForm(forms.ModelForm):
    """Form for creating/updating classrooms"""
    
    class Meta:
        model = ClassRoom
        fields = ['name', 'section', 'class_teacher']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'section': forms.TextInput(attrs={'class': 'form-control'}),
            'class_teacher': forms.Select(attrs={'class': 'form-control'}),
        }


# ==================== Subject Form ====================
class SubjectForm(forms.ModelForm):
    """Form for creating/updating subjects"""
    
    class Meta:
        model = Subject
        fields = ['name', 'code', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


# ==================== Attendance Form ====================
class AttendanceForm(forms.ModelForm):
    """Form for marking attendance"""
    
    class Meta:
        model = Attendance
        fields = ['student', 'subject', 'date', 'status', 'remarks']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


# ==================== Notice Form ====================
class NoticeForm(forms.ModelForm):
    """Form for creating notices"""
    
    class Meta:
        model = Notice
        fields = ['title', 'content', 'target_role', 'publish_date', 'expiry_date', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'target_role': forms.Select(attrs={'class': 'form-control'}),
            'publish_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


# ==================== Assignment Form ====================
class AssignmentForm(forms.ModelForm):
    """Form for creating assignments"""
    
    class Meta:
        model = Assignment
        fields = ['title', 'description', 'subject', 'classroom', 'file', 'due_date', 'total_marks']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'classroom': forms.Select(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
        }


# ==================== Submission Form ====================
class SubmissionForm(forms.ModelForm):
    """Form for submitting assignments"""
    
    class Meta:
        model = Submission
        fields = ['file']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ==================== Result Form ====================
class ResultForm(forms.ModelForm):
    """Form for entering exam results"""
    
    class Meta:
        model = Result
        fields = ['student', 'subject', 'exam_name', 'exam_date', 'marks', 'total_marks', 'grade']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'exam_name': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'marks': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'total_marks': forms.NumberInput(attrs={'class': 'form-control'}),
            'grade': forms.TextInput(attrs={'class': 'form-control'}),
        }
