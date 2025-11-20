"""
Models for Smart School Management Portal

This module contains all database models including:
- Custom User model with role-based access (Admin, Teacher, Student)
- ClassRoom: Represents classes/grades/sections
- Subject: Academic subjects
- Teacher: Teacher profile linked to User
- Student: Student profile linked to User
- Attendance: Daily attendance records
- Notice: Announcements and notices
- Assignment: Teacher-created assignments
- Submission: Student assignment submissions
- Result: Exam marks and results
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Avg, Count
from datetime import timedelta


# ==================== Custom User Model ====================
class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    
    Adds role field to distinguish between admin, teacher, and student.
    This allows role-based access control throughout the application.
    
    Fields:
        role: CharField with choices (admin, teacher, student)
        + all fields from AbstractUser (username, email, password, etc.)
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES,
        help_text="User role in the system"
    )
    
    # Profile fields
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', 
        blank=True, 
        null=True
    )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['username']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
    
    def get_full_name(self):
        """Return the first_name plus the last_name, with a space in between."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name if full_name else self.username


# ==================== ClassRoom Model ====================
class ClassRoom(models.Model):
    """
    Represents a class/grade/section in the school.
    
    Examples: "10th Grade - A", "9th Grade - B", "Grade 5"
    
    Fields:
        name: Name of the class
        section: Optional section identifier
        class_teacher: Optional teacher assigned to this class
        created_at: Timestamp of creation
    """
    name = models.CharField(
        max_length=100,
        help_text="Class name (e.g., '10th Grade', 'Class 5')"
    )
    section = models.CharField(
        max_length=10, 
        blank=True, 
        null=True,
        help_text="Section (e.g., 'A', 'B', 'C')"
    )
    class_teacher = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_classes'
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Class Room'
        verbose_name_plural = 'Class Rooms'
        ordering = ['name', 'section']
        unique_together = ('name', 'section')

    def __str__(self):
        if self.section:
            return f"{self.name} - {self.section}"
        return self.name


# ==================== Subject Model ====================
class Subject(models.Model):
    """
    Represents an academic subject.
    
    Fields:
        name: Subject name (e.g., Mathematics, Physics)
        code: Optional subject code (e.g., MATH101)
        description: Optional subject description
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Subject name"
    )
    code = models.CharField(
        max_length=20, 
        blank=True, 
        null=True,
        unique=True,
        help_text="Subject code (e.g., MATH101)"
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        ordering = ['name']

    def __str__(self):
        if self.code:
            return f"{self.name} ({self.code})"
        return self.name


# ==================== Teacher Model ====================
class Teacher(models.Model):
    """
    Teacher profile linked to User model via OneToOneField.
    
    Fields:
        user: Link to User model (one-to-one)
        subjects: Many-to-many relation with Subject
        phone: Contact number
        qualification: Educational qualification
        experience_years: Years of teaching experience
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )
    subjects = models.ManyToManyField(
        Subject, 
        blank=True,
        related_name='teachers'
    )
    qualification = models.CharField(max_length=200, blank=True, null=True)
    experience_years = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)]
    )
    joining_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        ordering = ['user__first_name', 'user__last_name']

    def __str__(self):
        return self.user.get_full_name()
    
    def get_subject_list(self):
        """Return comma-separated list of subjects"""
        return ", ".join([subject.name for subject in self.subjects.all()])


# ==================== Student Model ====================
class Student(models.Model):
    """
    Student profile linked to User model via OneToOneField.
    
    Fields:
        user: Link to User model (one-to-one)
        roll_no: Unique student roll number
        classroom: Link to ClassRoom
        parent_name: Guardian/parent name
        parent_phone: Guardian/parent contact
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    roll_no = models.CharField(
        max_length=30, 
        unique=True,
        help_text="Student roll number"
    )
    classroom = models.ForeignKey(
        ClassRoom, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='students'
    )
    parent_name = models.CharField(max_length=200, blank=True, null=True)
    parent_phone = models.CharField(max_length=20, blank=True, null=True)
    admission_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        ordering = ['roll_no']

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.roll_no}"


# ==================== Attendance Model ====================
class Attendance(models.Model):
    """
    Daily attendance record for students.
    
    Fields:
        student: Link to Student
        subject: Optional link to Subject (for subject-wise attendance)
        date: Attendance date
        status: Present/Absent/Leave
        marked_by: Teacher who marked attendance
        remarks: Optional notes
    
    Constraints:
        unique_together: (student, date, subject) - prevents duplicate entries
    """
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('leave', 'Leave'),
    )
    
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='attendance_records'
    )
    date = models.DateField(default=timezone.now)
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES,
        default='present'
    )
    marked_by = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='marked_attendances'
    )
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = ('student', 'date', 'subject')
        ordering = ['-date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"


# ==================== Notice Model ====================
class Notice(models.Model):
    """
    Notice/Announcement model for school-wide or targeted announcements.
    
    Fields:
        title: Notice title
        content: Notice content/description
        created_by: User who created the notice
        target_role: Optional role targeting (all, teacher, student)
        publish_date: When notice becomes visible
        expiry_date: Optional expiration date
        is_active: Whether notice is currently active
    """
    TARGET_CHOICES = (
        ('all', 'All'),
        ('teacher', 'Teachers Only'),
        ('student', 'Students Only'),
    )
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_notices'
    )
    target_role = models.CharField(
        max_length=20,
        choices=TARGET_CHOICES,
        default='all'
    )
    publish_date = models.DateField(default=timezone.now)
    expiry_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Notice'
        verbose_name_plural = 'Notices'
        ordering = ['-publish_date', '-created_at']

    def __str__(self):
        return self.title


# ==================== Assignment Model ====================
class Assignment(models.Model):
    """
    Assignment created by teachers.
    
    Fields:
        title: Assignment title
        description: Assignment instructions
        subject: Related subject
        classroom: Target classroom
        uploaded_by: Teacher who created it
        file: Optional attachment
        due_date: Submission deadline
        total_marks: Maximum marks
    """
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='assignments'
    )
    classroom = models.ForeignKey(
        ClassRoom,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assignments'
    )
    uploaded_by = models.ForeignKey(
        Teacher, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_assignments'
    )
    file = models.FileField(
        upload_to='assignments/', 
        blank=True, 
        null=True
    )
    due_date = models.DateField(null=True, blank=True)
    total_marks = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)]
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Assignment'
        verbose_name_plural = 'Assignments'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# ==================== Submission Model ====================
class Submission(models.Model):
    """
    Student submission for assignments.
    
    Fields:
        assignment: Link to Assignment
        student: Link to Student
        file: Submitted file
        submitted_at: Submission timestamp
        remarks: Teacher feedback
        marks_obtained: Marks awarded
        is_late: Whether submitted after deadline
    """
    assignment = models.ForeignKey(
        Assignment, 
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    file = models.FileField(upload_to='submissions/')
    submitted_at = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(blank=True, null=True)
    marks_obtained = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    is_late = models.BooleanField(default=False)
    graded_at = models.DateTimeField(null=True, blank=True)
    graded_by = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='graded_submissions'
    )

    class Meta:
        verbose_name = 'Submission'
        verbose_name_plural = 'Submissions'
        unique_together = ('assignment', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student} - {self.assignment}"


# ==================== Result Model ====================
class Result(models.Model):
    """
    Exam results/marks for students.
    
    Fields:
        student: Link to Student
        subject: Link to Subject
        marks: Marks obtained
        exam_name: Name of exam (e.g., Midterm, Final)
        exam_date: Date of exam
        total_marks: Maximum marks for the exam
    """
    student = models.ForeignKey(
        Student, 
        on_delete=models.CASCADE,
        related_name='results'
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='results'
    )
    marks = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    total_marks = models.IntegerField(
        default=100,
        validators=[MinValueValidator(0)]
    )
    exam_name = models.CharField(max_length=100)
    exam_date = models.DateField(default=timezone.now)
    grade = models.CharField(max_length=5, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        ordering = ['-exam_date']
        unique_together = ('student', 'subject', 'exam_name')

    def __str__(self):
        return f"{self.student} - {self.exam_name} - {self.marks}/{self.total_marks}"
    
    def calculate_percentage(self):
        """Calculate percentage score"""
        if self.total_marks > 0:
            return (float(self.marks) / float(self.total_marks)) * 100
        return 0
    
    def save(self, *args, **kwargs):
        """Auto-calculate grade based on percentage"""
        if not self.grade:
            percentage = self.calculate_percentage()
            if percentage >= 90:
                self.grade = 'A+'
            elif percentage >= 80:
                self.grade = 'A'
            elif percentage >= 70:
                self.grade = 'B'
            elif percentage >= 60:
                self.grade = 'C'
            elif percentage >= 50:
                self.grade = 'D'
            else:
                self.grade = 'F'
        super().save(*args, **kwargs)


# ==================== ADVANCED FEATURES ====================

# ==================== Timetable Model ====================
class Timetable(models.Model):
    """
    Class timetable/schedule management.
    
    Allows creating weekly schedules for different classes.
    """
    WEEKDAY_CHOICES = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
    )
    
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='timetable_entries')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    weekday = models.CharField(max_length=10, choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = 'Timetable Entry'
        verbose_name_plural = 'Timetable'
        ordering = ['weekday', 'start_time']
        unique_together = ('classroom', 'weekday', 'start_time')
    
    def __str__(self):
        return f"{self.classroom} - {self.get_weekday_display()} {self.start_time}-{self.end_time}"


# ==================== Exam Model ====================
class Exam(models.Model):
    """
    Exam/Test management with schedule.
    """
    EXAM_TYPE_CHOICES = (
        ('midterm', 'Mid-term Exam'),
        ('final', 'Final Exam'),
        ('quiz', 'Quiz'),
        ('test', 'Class Test'),
        ('practical', 'Practical Exam'),
    )
    
    name = models.CharField(max_length=200)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPE_CHOICES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField(default=100)
    instructions = models.TextField(blank=True)
    created_by = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    is_published = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.name} - {self.subject.name} ({self.date})"


# ==================== Leave Application Model ====================
class LeaveApplication(models.Model):
    """
    Student/Teacher leave application system.
    """
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_applications')
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    applied_on = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_leaves')
    reviewed_on = models.DateTimeField(null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Leave Application'
        verbose_name_plural = 'Leave Applications'
        ordering = ['-applied_on']
    
    def __str__(self):
        return f"{self.applicant.get_full_name()} - {self.start_date} to {self.end_date}"
    
    def get_duration(self):
        """Calculate leave duration in days"""
        return (self.end_date - self.start_date).days + 1


# ==================== Fee Management Model ====================
class Fee(models.Model):
    """
    Student fee management system.
    """
    FEE_TYPE_CHOICES = (
        ('tuition', 'Tuition Fee'),
        ('library', 'Library Fee'),
        ('lab', 'Laboratory Fee'),
        ('sports', 'Sports Fee'),
        ('exam', 'Examination Fee'),
        ('transport', 'Transport Fee'),
        ('other', 'Other'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('partial', 'Partially Paid'),
        ('overdue', 'Overdue'),
    )
    
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    fee_type = models.CharField(max_length=20, choices=FEE_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    academic_year = models.CharField(max_length=20, default='2025-26')
    semester = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Fee'
        verbose_name_plural = 'Fees'
        ordering = ['-due_date']
    
    def __str__(self):
        return f"{self.student.roll_no} - {self.get_fee_type_display()} - {self.amount}"
    
    def get_balance(self):
        """Calculate remaining balance"""
        return float(self.amount) - float(self.paid_amount)
    
    def save(self, *args, **kwargs):
        """Auto-update payment status"""
        if self.paid_amount >= self.amount:
            self.payment_status = 'paid'
        elif self.paid_amount > 0:
            self.payment_status = 'partial'
        elif self.due_date < timezone.now().date() and self.paid_amount == 0:
            self.payment_status = 'overdue'
        super().save(*args, **kwargs)


# ==================== Communication/Message Model ====================
class Message(models.Model):
    """
    Internal messaging system for communication.
    """
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    parent_message = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')
    
    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"From {self.sender.username} to {self.recipient.username}: {self.subject}"
    
    def mark_as_read(self):
        """Mark message as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()


# ==================== Event/Activity Model ====================
class Event(models.Model):
    """
    School events, activities, and holidays.
    """
    EVENT_TYPE_CHOICES = (
        ('academic', 'Academic Event'),
        ('sports', 'Sports Event'),
        ('cultural', 'Cultural Event'),
        ('holiday', 'Holiday'),
        ('meeting', 'Meeting'),
        ('exam', 'Examination'),
        ('other', 'Other'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    location = models.CharField(max_length=200, blank=True)
    organized_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    target_audience = models.CharField(max_length=20, choices=[('all', 'All'), ('student', 'Students'), ('teacher', 'Teachers')], default='all')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        ordering = ['start_date']
    
    def __str__(self):
        return f"{self.title} ({self.start_date})"


# ==================== Library Book Model ====================
class LibraryBook(models.Model):
    """
    Library book management system.
    """
    title = models.CharField(max_length=300)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=20, unique=True)
    category = models.CharField(max_length=100)
    publisher = models.CharField(max_length=200, blank=True)
    publication_year = models.IntegerField(null=True, blank=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    shelf_location = models.CharField(max_length=50, blank=True)
    added_on = models.DateField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Library Book'
        verbose_name_plural = 'Library Books'
        ordering = ['title']
    
    def __str__(self):
        return f"{self.title} by {self.author}"
    
    def is_available(self):
        """Check if book is available for borrowing"""
        return self.available_copies > 0


# ==================== Book Issue Model ====================
class BookIssue(models.Model):
    """
    Track book borrowing/issuing to students.
    """
    book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE, related_name='issues')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='borrowed_books')
    issue_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_returned = models.BooleanField(default=False)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='issued_books')
    
    class Meta:
        verbose_name = 'Book Issue'
        verbose_name_plural = 'Book Issues'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.book.title} - {self.student.user.get_full_name()}"
    
    def calculate_fine(self):
        """Calculate fine for late return (₹5 per day)"""
        if self.return_date and self.return_date > self.due_date:
            days_late = (self.return_date - self.due_date).days
            self.fine_amount = days_late * 5
            self.save()
        elif not self.is_returned and timezone.now().date() > self.due_date:
            days_late = (timezone.now().date() - self.due_date).days
            return days_late * 5
        return 0


# ==================== Meeting Portal Model ====================
class Meeting(models.Model):
    """
    Meeting management system for Principal to conduct meetings
    with staff, students, and parents.
    """
    MEETING_TYPE_CHOICES = (
        ('staff', 'Staff Meeting'),
        ('parent', 'Parent Meeting'),
        ('student', 'Student Meeting'),
        ('general', 'General Meeting'),
    )
    
    STATUS_CHOICES = (
        ('scheduled', 'Scheduled'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    title = models.CharField(max_length=200, help_text="Meeting title")
    meeting_type = models.CharField(max_length=20, choices=MEETING_TYPE_CHOICES)
    description = models.TextField(help_text="Meeting agenda and details")
    topic = models.CharField(max_length=300, help_text="Main discussion topic")
    
    # Meeting Schedule
    meeting_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    location = models.CharField(max_length=200, help_text="Meeting venue")
    
    # Organizer (Principal/Admin)
    organized_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='organized_meetings',
        help_text="Principal or admin organizing the meeting"
    )
    
    # Participants
    participants = models.ManyToManyField(
        User, 
        related_name='meetings_attending',
        blank=True,
        help_text="Users invited to the meeting"
    )
    
    # Meeting Details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    is_virtual = models.BooleanField(default=False, help_text="Is this an online meeting?")
    meeting_link = models.URLField(blank=True, null=True, help_text="Online meeting link (Zoom, Google Meet, etc.)")
    
    # Notes and Minutes
    meeting_notes = models.TextField(blank=True, null=True, help_text="Meeting minutes and notes")
    action_items = models.TextField(blank=True, null=True, help_text="Action items and decisions")
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Meeting'
        verbose_name_plural = 'Meetings'
        ordering = ['-meeting_date', '-start_time']
    
    def __str__(self):
        return f"{self.title} - {self.get_meeting_type_display()} ({self.meeting_date})"
    
    def is_upcoming(self):
        """Check if meeting is in the future"""
        from datetime import datetime
        meeting_datetime = datetime.combine(self.meeting_date, self.start_time)
        return meeting_datetime > timezone.now() and self.status == 'scheduled'
    
    def is_today(self):
        """Check if meeting is today"""
        return self.meeting_date == timezone.now().date()
    
    def get_duration(self):
        """Calculate meeting duration"""
        from datetime import datetime
        start = datetime.combine(self.meeting_date, self.start_time)
        end = datetime.combine(self.meeting_date, self.end_time)
        duration = end - start
        hours = duration.seconds // 3600
        minutes = (duration.seconds % 3600) // 60
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"
