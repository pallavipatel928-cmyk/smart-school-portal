"""
Django Admin Configuration for Smart School Management Portal

This file registers all models with the Django admin interface
and customizes their display and functionality.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, Teacher, Student, ClassRoom, Subject,
    Attendance, Notice, Assignment, Submission, Result,
    Timetable, Exam, LeaveApplication, Fee, Message, Event, LibraryBook, BookIssue, Meeting
)


# ==================== Custom User Admin ====================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Custom admin for User model.
    Extends Django's built-in UserAdmin to include role field.
    """
    # Add role to the fieldsets
    fieldsets = (
        *BaseUserAdmin.fieldsets,
        ('Role & Profile', {
            'fields': ('role', 'phone', 'address', 'date_of_birth', 'profile_picture')
        }),
    )
    
    # Add role to the add_fieldsets
    add_fieldsets = (
        *BaseUserAdmin.add_fieldsets,
        ('Role Information', {
            'fields': ('role',)
        }),
    )
    
    list_display = ('username', 'email', 'role', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('username', 'email', 'first_name', 'last_name')


# ==================== ClassRoom Admin ====================
@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    """Admin for ClassRoom model"""
    list_display = ('name', 'section', 'class_teacher', 'created_at')
    list_filter = ('name', 'section')
    search_fields = ('name', 'section')
    raw_id_fields = ('class_teacher',)


# ==================== Subject Admin ====================
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    """Admin for Subject model"""
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')


# ==================== Teacher Admin ====================
@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    """Admin for Teacher model"""
    list_display = ('user', 'get_full_name', 'qualification', 'experience_years', 'is_active', 'joining_date')
    list_filter = ('is_active', 'joining_date', 'subjects')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'qualification')
    filter_horizontal = ('subjects',)
    raw_id_fields = ('user',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


# ==================== Student Admin ====================
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    """Admin for Student model"""
    list_display = ('roll_no', 'user', 'get_full_name', 'classroom', 'is_active', 'admission_date')
    list_filter = ('is_active', 'classroom', 'admission_date')
    search_fields = ('roll_no', 'user__username', 'user__first_name', 'user__last_name', 'parent_name')
    raw_id_fields = ('user',)
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = 'Full Name'


# ==================== Attendance Admin ====================
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin for Attendance model"""
    list_display = ('student', 'date', 'status', 'subject', 'marked_by')
    list_filter = ('status', 'date', 'subject')
    search_fields = ('student__user__username', 'student__roll_no')
    date_hierarchy = 'date'
    raw_id_fields = ('student', 'marked_by')


# ==================== Notice Admin ====================
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    """Admin for Notice model"""
    list_display = ('title', 'target_role', 'publish_date', 'expiry_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'target_role', 'publish_date')
    search_fields = ('title', 'content')
    date_hierarchy = 'publish_date'
    raw_id_fields = ('created_by',)


# ==================== Assignment Admin ====================
@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin for Assignment model"""
    list_display = ('title', 'subject', 'classroom', 'uploaded_by', 'due_date', 'total_marks', 'created_at')
    list_filter = ('subject', 'classroom', 'due_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'due_date'
    raw_id_fields = ('uploaded_by',)


# ==================== Submission Admin ====================
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Admin for Submission model"""
    list_display = ('assignment', 'student', 'submitted_at', 'marks_obtained', 'is_late', 'graded_by')
    list_filter = ('is_late', 'submitted_at', 'assignment')
    search_fields = ('student__user__username', 'student__roll_no', 'assignment__title')
    date_hierarchy = 'submitted_at'
    raw_id_fields = ('student', 'graded_by')


# ==================== Result Admin ====================
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    """Admin for Result model"""
    list_display = ('student', 'subject', 'exam_name', 'marks', 'total_marks', 'grade', 'exam_date')
    list_filter = ('exam_name', 'subject', 'exam_date', 'grade')
    search_fields = ('student__user__username', 'student__roll_no', 'exam_name')
    date_hierarchy = 'exam_date'
    raw_id_fields = ('student',)


# Customize admin site header and title
admin.site.site_header = "Smart School Management Portal"
admin.site.site_title = "School Admin"
admin.site.index_title = "Welcome to Smart School Administration"


# ==================== ADVANCED FEATURES ADMIN ====================

# ==================== Timetable Admin ====================
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    """Admin for Timetable model"""
    list_display = ('classroom', 'subject', 'teacher', 'weekday', 'start_time', 'end_time', 'room_number')
    list_filter = ('weekday', 'classroom', 'subject')
    search_fields = ('classroom__name', 'subject__name', 'room_number')
    raw_id_fields = ('teacher',)


# ==================== Exam Admin ====================
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    """Admin for Exam model"""
    list_display = ('name', 'exam_type', 'subject', 'classroom', 'date', 'start_time', 'total_marks', 'is_published')
    list_filter = ('exam_type', 'is_published', 'date', 'subject', 'classroom')
    search_fields = ('name', 'subject__name', 'classroom__name')
    date_hierarchy = 'date'
    raw_id_fields = ('created_by',)


# ==================== Leave Application Admin ====================
@admin.register(LeaveApplication)
class LeaveApplicationAdmin(admin.ModelAdmin):
    """Admin for Leave Application model"""
    list_display = ('applicant', 'start_date', 'end_date', 'get_duration', 'status', 'applied_on', 'reviewed_by')
    list_filter = ('status', 'applied_on', 'start_date')
    search_fields = ('applicant__username', 'applicant__first_name', 'applicant__last_name', 'reason')
    date_hierarchy = 'applied_on'
    raw_id_fields = ('applicant', 'reviewed_by')
    
    def get_duration(self, obj):
        return f"{obj.get_duration()} days"
    get_duration.short_description = 'Duration'


# ==================== Fee Admin ====================
@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    """Admin for Fee model"""
    list_display = ('student', 'fee_type', 'amount', 'paid_amount', 'get_balance', 'payment_status', 'due_date', 'payment_date')
    list_filter = ('payment_status', 'fee_type', 'academic_year', 'due_date')
    search_fields = ('student__roll_no', 'student__user__username', 'transaction_id')
    date_hierarchy = 'due_date'
    raw_id_fields = ('student',)
    
    def get_balance(self, obj):
        return f"₹{obj.get_balance():.2f}"
    get_balance.short_description = 'Balance'


# ==================== Message Admin ====================
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin for Message model"""
    list_display = ('sender', 'recipient', 'subject', 'sent_at', 'is_read', 'read_at')
    list_filter = ('is_read', 'sent_at')
    search_fields = ('sender__username', 'recipient__username', 'subject', 'body')
    date_hierarchy = 'sent_at'
    raw_id_fields = ('sender', 'recipient')


# ==================== Event Admin ====================
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    """Admin for Event model"""
    list_display = ('title', 'event_type', 'start_date', 'end_date', 'location', 'target_audience', 'is_active')
    list_filter = ('event_type', 'target_audience', 'is_active', 'start_date')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'start_date'
    raw_id_fields = ('organized_by',)


# ==================== Library Book Admin ====================
@admin.register(LibraryBook)
class LibraryBookAdmin(admin.ModelAdmin):
    """Admin for Library Book model"""
    list_display = ('title', 'author', 'isbn', 'category', 'total_copies', 'available_copies', 'is_available')
    list_filter = ('category', 'publication_year')
    search_fields = ('title', 'author', 'isbn', 'publisher')
    
    def is_available(self, obj):
        return obj.is_available()
    is_available.boolean = True
    is_available.short_description = 'Available'


# ==================== Book Issue Admin ====================
@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    """Admin for Book Issue model"""
    list_display = ('book', 'student', 'issue_date', 'due_date', 'return_date', 'fine_amount', 'is_returned')
    list_filter = ('is_returned', 'issue_date', 'due_date')
    search_fields = ('book__title', 'student__roll_no', 'student__user__username')
    date_hierarchy = 'issue_date'
    raw_id_fields = ('student', 'issued_by')


# ==================== Meeting Portal Admin ====================
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Admin for Meeting Portal model"""
    list_display = ('title', 'meeting_type', 'meeting_date', 'start_time', 'status', 'organized_by', 'location')
    list_filter = ('meeting_type', 'status', 'is_virtual', 'meeting_date')
    search_fields = ('title', 'topic', 'description', 'location')
    date_hierarchy = 'meeting_date'
    filter_horizontal = ('participants',)
    raw_id_fields = ('organized_by',)
    
    fieldsets = (
        ('Meeting Information', {
            'fields': ('title', 'meeting_type', 'topic', 'description')
        }),
        ('Schedule', {
            'fields': ('meeting_date', 'start_time', 'end_time', 'location')
        }),
        ('Virtual Meeting', {
            'fields': ('is_virtual', 'meeting_link')
        }),
        ('Organizer & Participants', {
            'fields': ('organized_by', 'participants')
        }),
        ('Status & Notes', {
            'fields': ('status', 'meeting_notes', 'action_items')
        }),
    )
