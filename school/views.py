"""
Views for Smart School Management Portal

This module contains all view functions and classes for handling
HTTP requests and rendering templates.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Avg
from django.utils import timezone
from datetime import datetime, timedelta

from .models import (
    User, Student, Teacher, ClassRoom, Subject,
    Attendance, Notice, Assignment, Submission, Result,
    Timetable, Exam, LeaveApplication, Fee, Message, Event, LibraryBook, BookIssue, Meeting
)
from .forms import (
    UserRegistrationForm, UserLoginForm, StudentForm, TeacherForm,
    AttendanceForm, NoticeForm, AssignmentForm, SubmissionForm, ResultForm
)


# ==================== Authentication Views ====================
def user_login(request):
    """
    Handle user login.
    GET: Display login form
    POST: Authenticate and login user
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'school/login.html', {'form': form})


def user_register(request):
    """
    Handle user registration.
    GET: Display registration form
    POST: Create new user account
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Admin needs to activate
            user.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'school/register.html', {'form': form})


@login_required
def user_logout(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')


# ==================== Dashboard Views ====================
@login_required
def dashboard(request):
    """
    Main dashboard view.
    Display different content based on user role.
    """
    user = request.user
    context = {'user': user}
    
    if user.role == 'student':
        # Student dashboard
        try:
            student = user.student_profile
            context.update({
                'student': student,
                'recent_notices': Notice.objects.filter(
                    Q(target_role='all') | Q(target_role='student'),
                    is_active=True,
                    publish_date__lte=timezone.now()
                ).order_by('-publish_date')[:5],
                'assignments': Assignment.objects.filter(
                    classroom=student.classroom
                ).order_by('-created_at')[:5],
                'recent_results': Result.objects.filter(student=student).order_by('-exam_date')[:5],
            })
        except Student.DoesNotExist:
            messages.warning(request, 'Please complete your student profile.')
    
    elif user.role == 'teacher':
        # Teacher dashboard
        try:
            teacher = user.teacher_profile
            context.update({
                'teacher': teacher,
                'recent_notices': Notice.objects.filter(
                    Q(target_role='all') | Q(target_role='teacher'),
                    is_active=True,
                    publish_date__lte=timezone.now()
                ).order_by('-publish_date')[:5],
                'my_assignments': Assignment.objects.filter(
                    uploaded_by=teacher
                ).order_by('-created_at')[:5],
                'subjects': teacher.subjects.all(),
            })
        except Teacher.DoesNotExist:
            messages.warning(request, 'Please complete your teacher profile.')
    
    elif user.role == 'admin' or user.is_staff:
        # Admin dashboard with statistics
        context.update({
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_subjects': Subject.objects.count(),
            'total_classes': ClassRoom.objects.count(),
            'recent_notices': Notice.objects.filter(is_active=True).order_by('-publish_date')[:5],
            'pending_users': User.objects.filter(is_active=False).count(),
        })
    
    return render(request, 'school/dashboard.html', context)


# ==================== Student Views ====================
@login_required
def student_list(request):
    """Display list of all students"""
    students = Student.objects.select_related('user', 'classroom').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        students = students.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(roll_no__icontains=search_query)
        )
    
    return render(request, 'school/student_list.html', {
        'students': students,
        'search_query': search_query
    })


@login_required
def student_detail(request, pk):
    """Display detailed information about a student"""
    student = get_object_or_404(Student, pk=pk)
    
    # Get student's attendance statistics
    total_attendance = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status='present').count()
    attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    context = {
        'student': student,
        'results': Result.objects.filter(student=student).order_by('-exam_date'),
        'attendance_percentage': round(attendance_percentage, 2),
        'total_attendance': total_attendance,
        'present_count': present_count,
    }
    
    return render(request, 'school/student_detail.html', context)


# ==================== Teacher Views ====================
@login_required
def teacher_list(request):
    """Display list of all teachers"""
    teachers = Teacher.objects.select_related('user').prefetch_related('subjects').filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        teachers = teachers.filter(
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(user__email__icontains=search_query) |
            Q(employee_id__icontains=search_query) |
            Q(subjects__name__icontains=search_query)
        ).distinct()
    
    return render(request, 'school/teacher_list.html', {
        'teachers': teachers,
        'search_query': search_query
    })


@login_required
def teacher_detail(request, pk):
    """Display detailed information about a teacher"""
    teacher = get_object_or_404(Teacher, pk=pk)
    
    context = {
        'teacher': teacher,
        'subjects': teacher.subjects.all(),
        'assignments': Assignment.objects.filter(uploaded_by=teacher).order_by('-created_at')[:10],
    }
    
    return render(request, 'school/teacher_detail.html', context)


# ==================== Attendance Views ====================
@login_required
def attendance_list(request):
    """Display attendance records"""
    attendances = Attendance.objects.select_related('student', 'subject', 'marked_by').order_by('-date')
    
    # Filter by date
    date_filter = request.GET.get('date', '')
    if date_filter:
        attendances = attendances.filter(date=date_filter)
    
    return render(request, 'school/attendance_list.html', {
        'attendances': attendances,
        'date_filter': date_filter
    })


@login_required
def mark_attendance(request):
    """Mark attendance for students"""
    if request.user.role != 'teacher' and not request.user.is_staff:
        messages.error(request, 'Only teachers can mark attendance.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            attendance = form.save(commit=False)
            if request.user.role == 'teacher':
                attendance.marked_by = request.user.teacher_profile
            attendance.save()
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance_list')
    else:
        form = AttendanceForm()
    
    return render(request, 'school/mark_attendance.html', {'form': form})


# ==================== Notice Views ====================
@login_required
def notice_list(request):
    """Display all notices"""
    notices = Notice.objects.filter(
        Q(target_role='all') | Q(target_role=request.user.role),
        is_active=True,
        publish_date__lte=timezone.now()
    ).order_by('-publish_date')
    
    return render(request, 'school/notice_list.html', {'notices': notices})


@login_required
def notice_create(request):
    """Create new notice (admin/teacher only)"""
    if request.user.role not in ['admin', 'teacher'] and not request.user.is_staff:
        messages.error(request, 'You do not have permission to create notices.')
        return redirect('notice_list')
    
    if request.method == 'POST':
        form = NoticeForm(request.POST)
        if form.is_valid():
            notice = form.save(commit=False)
            notice.created_by = request.user
            notice.save()
            messages.success(request, 'Notice created successfully.')
            return redirect('notice_list')
    else:
        form = NoticeForm()
    
    return render(request, 'school/notice_form.html', {'form': form})


# ==================== Assignment Views ====================
@login_required
def assignment_list(request):
    """Display assignments"""
    if request.user.role == 'student':
        try:
            student = request.user.student_profile
            assignments = Assignment.objects.filter(classroom=student.classroom).order_by('-created_at')
        except Student.DoesNotExist:
            assignments = Assignment.objects.none()
    elif request.user.role == 'teacher':
        teacher = request.user.teacher_profile
        assignments = Assignment.objects.filter(uploaded_by=teacher).order_by('-created_at')
    else:
        assignments = Assignment.objects.all().order_by('-created_at')
    
    return render(request, 'school/assignment_list.html', {'assignments': assignments})


@login_required
def assignment_create(request):
    """Create new assignment (teacher only)"""
    if request.user.role != 'teacher' and not request.user.is_staff:
        messages.error(request, 'Only teachers can create assignments.')
        return redirect('assignment_list')
    
    if request.method == 'POST':
        form = AssignmentForm(request.POST, request.FILES)
        if form.is_valid():
            assignment = form.save(commit=False)
            if request.user.role == 'teacher':
                assignment.uploaded_by = request.user.teacher_profile
            assignment.save()
            messages.success(request, 'Assignment created successfully.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    
    return render(request, 'school/assignment_form.html', {'form': form})


@login_required
def assignment_detail(request, pk):
    """Display assignment details and submissions"""
    assignment = get_object_or_404(Assignment, pk=pk)
    
    context = {'assignment': assignment}
    
    if request.user.role == 'student':
        try:
            student = request.user.student_profile
            try:
                submission = Submission.objects.get(assignment=assignment, student=student)
                context['my_submission'] = submission
            except Submission.DoesNotExist:
                context['my_submission'] = None
        except Student.DoesNotExist:
            pass
    else:
        # Teachers and admins can see all submissions
        context['submissions'] = Submission.objects.filter(assignment=assignment).select_related('student')
    
    return render(request, 'school/assignment_detail.html', context)


@login_required
def submit_assignment(request, assignment_id):
    """Submit assignment (student only)"""
    if request.user.role != 'student':
        messages.error(request, 'Only students can submit assignments.')
        return redirect('assignment_list')
    
    assignment = get_object_or_404(Assignment, pk=assignment_id)
    student = request.user.student_profile
    
    # Check if already submitted
    existing_submission = Submission.objects.filter(assignment=assignment, student=student).first()
    if existing_submission:
        messages.warning(request, 'You have already submitted this assignment.')
        return redirect('assignment_detail', pk=assignment_id)
    
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.assignment = assignment
            submission.student = student
            # Check if late
            if assignment.due_date and timezone.now().date() > assignment.due_date:
                submission.is_late = True
            submission.save()
            messages.success(request, 'Assignment submitted successfully.')
            return redirect('assignment_detail', pk=assignment_id)
    else:
        form = SubmissionForm()
    
    return render(request, 'school/submit_assignment.html', {
        'form': form,
        'assignment': assignment
    })


# ==================== Result Views ====================
@login_required
def result_list(request):
    """Display exam results"""
    if request.user.role == 'student':
        try:
            student = request.user.student_profile
            results = Result.objects.filter(student=student).order_by('-exam_date')
        except Student.DoesNotExist:
            results = Result.objects.none()
    else:
        results = Result.objects.all().order_by('-exam_date')
    
    return render(request, 'school/result_list.html', {'results': results})


@login_required
def result_create(request):
    """Create exam result (teacher/admin only)"""
    if request.user.role not in ['teacher', 'admin'] and not request.user.is_staff:
        messages.error(request, 'You do not have permission to add results.')
        return redirect('result_list')
    
    if request.method == 'POST':
        form = ResultForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Result added successfully.')
            return redirect('result_list')
    else:
        form = ResultForm()
    
    return render(request, 'school/result_form.html', {'form': form})


# ==================== Profile View ====================
@login_required
def profile(request):
    """Display and edit user profile"""
    user = request.user
    
    context = {'user': user}
    
    if user.role == 'student':
        try:
            context['student'] = user.student_profile
        except Student.DoesNotExist:
            pass
    elif user.role == 'teacher':
        try:
            context['teacher'] = user.teacher_profile
        except Teacher.DoesNotExist:
            pass
    
    return render(request, 'school/profile.html', context)


# ==================== Home Page ====================
def home(request):
    """Home page / landing page"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    return render(request, 'school/home.html')


# ==================== ADVANCED FEATURES VIEWS ====================

# ==================== Timetable Views ====================
@login_required
def timetable_view(request):
    """View timetable based on user role"""
    user = request.user
    context = {}
    
    if user.role == 'student':
        try:
            student = user.student_profile
            if student.classroom:
                timetable = Timetable.objects.filter(classroom=student.classroom).select_related('subject', 'teacher').order_by('weekday', 'start_time')
                context['timetable'] = timetable
                context['classroom'] = student.classroom
        except Student.DoesNotExist:
            messages.warning(request, 'Please complete your student profile.')
    elif user.role == 'teacher':
        try:
            teacher = user.teacher_profile
            timetable = Timetable.objects.filter(teacher=teacher).select_related('subject', 'classroom').order_by('weekday', 'start_time')
            context['timetable'] = timetable
        except Teacher.DoesNotExist:
            pass
    else:
        # Admin can view all
        timetable = Timetable.objects.all().select_related('subject', 'teacher', 'classroom').order_by('classroom', 'weekday', 'start_time')
        context['timetable'] = timetable
    
    return render(request, 'school/timetable.html', context)


# ==================== Exam Views ====================
@login_required
def exam_list(request):
    """Display upcoming and past exams"""
    user = request.user
    
    if user.role == 'student':
        try:
            student = user.student_profile
            exams = Exam.objects.filter(classroom=student.classroom, is_published=True).order_by('-date')
        except Student.DoesNotExist:
            exams = Exam.objects.none()
    elif user.role == 'teacher':
        try:
            teacher = user.teacher_profile
            exams = Exam.objects.filter(created_by=teacher).order_by('-date')
        except Teacher.DoesNotExist:
            exams = Exam.objects.none()
    else:
        exams = Exam.objects.all().order_by('-date')
    
    return render(request, 'school/exam_list.html', {'exams': exams})


# ==================== Leave Application Views ====================
@login_required
def leave_application_list(request):
    """Display leave applications"""
    user = request.user
    
    if user.role in ['admin', 'teacher']:
        # Admin and teachers can see all pending applications
        applications = LeaveApplication.objects.all().select_related('applicant').order_by('-applied_on')
    else:
        # Students see only their own applications
        applications = LeaveApplication.objects.filter(applicant=user).order_by('-applied_on')
    
    return render(request, 'school/leave_list.html', {'applications': applications})


@login_required
def apply_leave(request):
    """Apply for leave"""
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        reason = request.POST.get('reason')
        
        LeaveApplication.objects.create(
            applicant=request.user,
            start_date=start_date,
            end_date=end_date,
            reason=reason
        )
        messages.success(request, 'Leave application submitted successfully!')
        return redirect('leave_list')
    
    return render(request, 'school/leave_apply.html')


@login_required
def leave_review(request, pk):
    """Approve or reject leave application (Admin/Teacher only)"""
    if request.user.role not in ['admin', 'teacher']:
        messages.error(request, 'You do not have permission to review leave applications.')
        return redirect('leave_list')
    
    leave = get_object_or_404(LeaveApplication, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        remarks = request.POST.get('remarks', '')
        
        leave.status = action
        leave.reviewed_by = request.user
        leave.reviewed_on = timezone.now()
        leave.remarks = remarks
        leave.save()
        
        messages.success(request, f'Leave application {action}!')
        return redirect('leave_list')
    
    return render(request, 'school/leave_review.html', {'leave': leave})


# ==================== Fee Management Views ====================
@login_required
def fee_list(request):
    """Display fee records"""
    user = request.user
    
    if user.role == 'student':
        try:
            student = user.student_profile
            fees = Fee.objects.filter(student=student).order_by('-due_date')
        except Student.DoesNotExist:
            fees = Fee.objects.none()
    else:
        # Admin can view all fees
        fees = Fee.objects.all().select_related('student').order_by('-due_date')
    
    return render(request, 'school/fee_list.html', {'fees': fees})


# ==================== Messaging System Views ====================
@login_required
def inbox(request):
    """Display user's inbox"""
    messages_list = Message.objects.filter(recipient=request.user).select_related('sender').order_by('-sent_at')
    unread_count = messages_list.filter(is_read=False).count()
    
    return render(request, 'school/inbox.html', {
        'messages': messages_list,
        'unread_count': unread_count
    })


@login_required
def message_detail(request, pk):
    """View message details"""
    message = get_object_or_404(Message, pk=pk, recipient=request.user)
    message.mark_as_read()
    
    return render(request, 'school/message_detail.html', {'message': message})


@login_required
def send_message(request):
    """Send a new message"""
    if request.method == 'POST':
        recipient_id = request.POST.get('recipient')
        subject = request.POST.get('subject')
        body = request.POST.get('body')
        
        recipient = get_object_or_404(User, pk=recipient_id)
        
        Message.objects.create(
            sender=request.user,
            recipient=recipient,
            subject=subject,
            body=body
        )
        
        messages.success(request, f'Message sent successfully to {recipient.get_full_name()}!')
        return redirect('inbox')
    
    # Get list of users to send message to
    users = User.objects.exclude(pk=request.user.pk).filter(is_active=True)
    
    # Pre-fill recipient and subject from URL parameters
    selected_recipient = request.GET.get('recipient', '')
    initial_subject = request.GET.get('subject', '')
    
    return render(request, 'school/send_message.html', {
        'users': users,
        'selected_recipient': selected_recipient,
        'initial_subject': initial_subject
    })


# ==================== Events/Calendar Views ====================
@login_required
def event_calendar(request):
    """Display school events calendar"""
    user = request.user
    events = Event.objects.filter(
        Q(target_audience='all') | Q(target_audience=user.role),
        is_active=True
    ).order_by('start_date')
    
    return render(request, 'school/event_calendar.html', {'events': events})


# ==================== Library Management Views ====================
@login_required
def library_books(request):
    """Display library books"""
    search_query = request.GET.get('search', '')
    books = LibraryBook.objects.all()
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    return render(request, 'school/library_books.html', {
        'books': books,
        'search_query': search_query
    })


@login_required
def my_borrowed_books(request):
    """Display student's borrowed books"""
    if request.user.role != 'student':
        messages.error(request, 'This feature is only for students.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
        borrowed_books = BookIssue.objects.filter(student=student).select_related('book').order_by('-issue_date')
    except Student.DoesNotExist:
        borrowed_books = BookIssue.objects.none()
    
    return render(request, 'school/my_books.html', {'borrowed_books': borrowed_books})


# ==================== Analytics & Reports ====================
@login_required
def student_analytics(request):
    """Advanced analytics for students"""
    if request.user.role != 'student':
        messages.error(request, 'This feature is only for students.')
        return redirect('dashboard')
    
    try:
        student = request.user.student_profile
        
        # Attendance analytics
        total_attendance = Attendance.objects.filter(student=student).count()
        present_count = Attendance.objects.filter(student=student, status='present').count()
        attendance_percentage = (present_count / total_attendance * 100) if total_attendance > 0 else 0
        
        # Grade analytics
        results = Result.objects.filter(student=student)
        average_percentage = results.aggregate(Avg('marks'))['marks__avg'] or 0
        
        # Subject-wise performance
        subject_performance = []
        for subject in Subject.objects.all():
            subject_results = results.filter(subject=subject)
            if subject_results.exists():
                avg = subject_results.aggregate(Avg('marks'))['marks__avg']
                subject_performance.append({
                    'subject': subject.name,
                    'average': round(avg, 2)
                })
        
        # Fee status
        pending_fees = Fee.objects.filter(student=student, payment_status__in=['pending', 'partial', 'overdue'])
        total_pending = sum(fee.get_balance() for fee in pending_fees)
        
        context = {
            'student': student,
            'attendance_percentage': round(attendance_percentage, 2),
            'average_percentage': round(average_percentage, 2),
            'subject_performance': subject_performance,
            'pending_fees': pending_fees,
            'total_pending': total_pending,
        }
        
        return render(request, 'school/student_analytics.html', context)
    except Student.DoesNotExist:
        messages.warning(request, 'Please complete your student profile.')
        return redirect('dashboard')


# ==================== Meeting Portal Views ====================
@login_required
def meeting_portal(request):
    """Display Meeting Portal dashboard"""
    user = request.user
    
    # Get meetings based on user role
    if user.role == 'admin' or user.is_staff:
        # Admin/Principal sees all meetings they organized
        my_meetings = Meeting.objects.filter(organized_by=user).order_by('-meeting_date', '-start_time')
        invited_meetings = Meeting.objects.filter(participants=user).exclude(organized_by=user).order_by('-meeting_date', '-start_time')
    else:
        # Teachers/Students see meetings they're invited to
        my_meetings = Meeting.objects.none()
        invited_meetings = Meeting.objects.filter(participants=user).order_by('-meeting_date', '-start_time')
    
    # Categorize meetings
    upcoming_meetings = [m for m in invited_meetings if m.is_upcoming()]
    today_meetings = [m for m in invited_meetings if m.is_today()]
    
    context = {
        'my_meetings': my_meetings[:10],
        'invited_meetings': invited_meetings[:10],
        'upcoming_meetings': upcoming_meetings[:5],
        'today_meetings': today_meetings,
        'can_create': user.role == 'admin' or user.is_staff,
    }
    
    return render(request, 'school/meeting_portal.html', context)


@login_required
def meeting_create(request):
    """Create a new meeting (Admin/Principal only)"""
    if not (request.user.role == 'admin' or request.user.is_staff):
        messages.error(request, 'Only administrators can create meetings.')
        return redirect('meeting_portal')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        meeting_type = request.POST.get('meeting_type')
        topic = request.POST.get('topic')
        description = request.POST.get('description')
        meeting_date = request.POST.get('meeting_date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        location = request.POST.get('location')
        is_virtual = request.POST.get('is_virtual') == 'on'
        meeting_link = request.POST.get('meeting_link', '')
        participant_ids = request.POST.getlist('participants')
        
        # Create meeting
        meeting = Meeting.objects.create(
            title=title,
            meeting_type=meeting_type,
            topic=topic,
            description=description,
            meeting_date=meeting_date,
            start_time=start_time,
            end_time=end_time,
            location=location,
            is_virtual=is_virtual,
            meeting_link=meeting_link if is_virtual else None,
            organized_by=request.user,
        )
        
        # Add participants
        if participant_ids:
            participants = User.objects.filter(pk__in=participant_ids)
            meeting.participants.set(participants)
        
        messages.success(request, f'Meeting "{title}" created successfully!')
        return redirect('meeting_detail', pk=meeting.pk)
    
    # Get users for participant selection
    users = User.objects.exclude(pk=request.user.pk).filter(is_active=True)
    
    return render(request, 'school/meeting_create.html', {'users': users})


@login_required
def meeting_detail(request, pk):
    """View meeting details"""
    meeting = get_object_or_404(Meeting, pk=pk)
    
    # Check if user has access
    if not (meeting.organized_by == request.user or request.user in meeting.participants.all()):
        messages.error(request, 'You do not have access to this meeting.')
        return redirect('meeting_portal')
    
    # Update meeting notes (organizer only)
    if request.method == 'POST' and meeting.organized_by == request.user:
        meeting_notes = request.POST.get('meeting_notes', '')
        action_items = request.POST.get('action_items', '')
        status = request.POST.get('status', meeting.status)
        
        meeting.meeting_notes = meeting_notes
        meeting.action_items = action_items
        meeting.status = status
        meeting.save()
        
        messages.success(request, 'Meeting updated successfully!')
        return redirect('meeting_detail', pk=pk)
    
    context = {
        'meeting': meeting,
        'is_organizer': meeting.organized_by == request.user,
        'is_participant': request.user in meeting.participants.all(),
    }
    
    return render(request, 'school/meeting_detail.html', context)
