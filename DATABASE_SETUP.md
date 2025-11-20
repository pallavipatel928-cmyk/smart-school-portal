# Database Configuration Guide

This guide covers how to set up different databases (SQLite, MySQL, MongoDB) for the Smart School Management Portal.

---

## 1. SQLite (Default - No Setup Required)

SQLite is the default database and requires **no additional setup**. It's perfect for development and testing.

**Configuration:** Already configured in `core/settings.py`

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

**Advantages:**
- No installation required
- Zero configuration
- Great for development

**Limitations:**
- Not suitable for production with multiple users
- No network access

---

## 2. MySQL Setup

### Step 1: Install MySQL Server

**Windows:**
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Run the installer and choose "Developer Default"
3. Set root password during installation
4. Complete the installation

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install mysql-server
sudo mysql_secure_installation
```

**macOS:**
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

### Step 2: Create Database

Login to MySQL:
```bash
mysql -u root -p
```

Create database and user:
```sql
CREATE DATABASE smartschool_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'schooladmin'@'localhost' IDENTIFIED BY 'YourStrongPassword123!';
GRANT ALL PRIVILEGES ON smartschool_db.* TO 'schooladmin'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 3: Install MySQL Client for Python

```bash
# Activate virtual environment first
pip install mysqlclient
```

**Note for Windows:** If mysqlclient installation fails, install from wheel:
```bash
pip install mysqlclient‑1.4.6‑cp311‑cp311‑win_amd64.whl
# Download wheel from: https://www.lfd.uci.edu/~gohlke/pythonlibs/#mysqlclient
```

### Step 4: Update Django Settings

Edit `core/settings.py` and replace the DATABASES configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'smartschool_db',
        'USER': 'schooladmin',
        'PASSWORD': 'YourStrongPassword123!',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### MySQL Raw Query Examples

```python
from django.db import connection

# Example 1: Get all students with attendance > 75%
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT s.roll_no, u.first_name, u.last_name,
               COUNT(CASE WHEN a.status = 'present' THEN 1 END) * 100.0 / COUNT(*) as attendance_percentage
        FROM school_student s
        JOIN school_user u ON s.user_id = u.id
        LEFT JOIN school_attendance a ON s.id = a.student_id
        GROUP BY s.id
        HAVING attendance_percentage > 75
    """)
    results = cursor.fetchall()

# Example 2: Get top 10 students by average marks
with connection.cursor() as cursor:
    cursor.execute("""
        SELECT s.roll_no, u.first_name, u.last_name, AVG(r.marks) as avg_marks
        FROM school_student s
        JOIN school_user u ON s.user_id = u.id
        JOIN school_result r ON s.id = r.student_id
        GROUP BY s.id
        ORDER BY avg_marks DESC
        LIMIT 10
    """)
    top_students = cursor.fetchall()
```

---

## 3. MongoDB Setup (Alternative for certain features)

MongoDB can be used alongside Django's primary database for specific features like logs, analytics, etc.

### Step 1: Install MongoDB

**Windows:**
1. Download from https://www.mongodb.com/try/download/community
2. Run installer and follow the wizard
3. MongoDB runs as a service automatically

**Linux (Ubuntu/Debian):**
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
sudo apt update
sudo apt install mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod
```

**macOS:**
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

### Step 2: Install Python Packages

```bash
pip install pymongo mongoengine
```

### Step 3: Configure MongoDB Connection

Add to `core/settings.py`:

```python
# MongoDB Configuration
from mongoengine import connect

MONGODB_DATABASES = {
    'default': {
        'name': 'smartschool_db',
        'host': 'localhost',
        'port': 27017,
    }
}

# Connect to MongoDB
connect(
    db=MONGODB_DATABASES['default']['name'],
    host=MONGODB_DATABASES['default']['host'],
    port=MONGODB_DATABASES['default']['port']
)
```

### Step 4: Create MongoDB Models (Example)

Create `school/mongo_models.py`:

```python
from mongoengine import Document, StringField, DateTimeField, IntField, ReferenceField
from datetime import datetime

class ActivityLog(Document):
    """MongoDB model for activity logging"""
    user_id = IntField(required=True)
    username = StringField(required=True, max_length=150)
    action = StringField(required=True, max_length=200)
    timestamp = DateTimeField(default=datetime.now)
    ip_address = StringField(max_length=45)
    details = StringField()
    
    meta = {
        'collection': 'activity_logs',
        'indexes': ['user_id', 'timestamp', 'action']
    }

class StudentAnalytics(Document):
    """MongoDB model for student analytics"""
    student_id = IntField(required=True, unique=True)
    roll_no = StringField(required=True)
    total_assignments = IntField(default=0)
    completed_assignments = IntField(default=0)
    average_marks = IntField(default=0)
    attendance_percentage = IntField(default=0)
    last_updated = DateTimeField(default=datetime.now)
    
    meta = {
        'collection': 'student_analytics',
        'indexes': ['student_id', 'roll_no']
    }
```

### MongoDB Query Examples

```python
from school.mongo_models import ActivityLog, StudentAnalytics

# Example 1: Log user activity
def log_activity(user, action, ip_address, details=''):
    ActivityLog(
        user_id=user.id,
        username=user.username,
        action=action,
        ip_address=ip_address,
        details=details
    ).save()

# Example 2: Get user activity history
def get_user_activity(user_id, limit=50):
    logs = ActivityLog.objects(user_id=user_id).order_by('-timestamp').limit(limit)
    return list(logs)

# Example 3: Update student analytics
def update_student_analytics(student):
    from school.models import Assignment, Result, Attendance
    
    total_assignments = Assignment.objects.filter(classroom=student.classroom).count()
    completed = student.submissions.count()
    avg_marks = Result.objects.filter(student=student).aggregate(Avg('marks'))['marks__avg'] or 0
    
    total_attendance = Attendance.objects.filter(student=student).count()
    present_count = Attendance.objects.filter(student=student, status='present').count()
    attendance_pct = (present_count / total_attendance * 100) if total_attendance > 0 else 0
    
    StudentAnalytics.objects(student_id=student.id).update_one(
        set__roll_no=student.roll_no,
        set__total_assignments=total_assignments,
        set__completed_assignments=completed,
        set__average_marks=int(avg_marks),
        set__attendance_percentage=int(attendance_pct),
        set__last_updated=datetime.now(),
        upsert=True
    )

# Example 4: Complex aggregation query
def get_class_performance_stats(classroom_id):
    from pymongo import MongoClient
    
    client = MongoClient('localhost', 27017)
    db = client.smartschool_db
    
    pipeline = [
        {
            '$group': {
                '_id': None,
                'avg_attendance': {'$avg': '$attendance_percentage'},
                'avg_marks': {'$avg': '$average_marks'},
                'total_students': {'$sum': 1},
                'high_performers': {
                    '$sum': {
                        '$cond': [{'$gte': ['$average_marks', 80]}, 1, 0]
                    }
                }
            }
        }
    ]
    
    results = list(db.student_analytics.aggregate(pipeline))
    return results[0] if results else None
```

---

## 4. Django ORM Query Examples

### Basic Queries

```python
from school.models import Student, Teacher, Attendance, Result, Assignment
from django.db.models import Count, Avg, Q, F, Sum

# Get all active students
students = Student.objects.filter(is_active=True)

# Get student with specific roll number
student = Student.objects.get(roll_no='2024001')

# Get students in a specific class
class_students = Student.objects.filter(classroom__name='10th Grade')

# Get all teachers teaching Mathematics
math_teachers = Teacher.objects.filter(subjects__name='Mathematics')
```

### Complex Queries

```python
# 1. Get students with attendance > 75%
from django.db.models import Count, Case, When, FloatField

students_high_attendance = Student.objects.annotate(
    total_days=Count('attendance_records'),
    present_days=Count('attendance_records', filter=Q(attendance_records__status='present')),
    attendance_pct=Case(
        When(total_days__gt=0, then=F('present_days') * 100.0 / F('total_days')),
        default=0,
        output_field=FloatField()
    )
).filter(attendance_pct__gt=75)

# 2. Get top 10 students by average marks
top_students = Student.objects.annotate(
    avg_marks=Avg('results__marks')
).order_by('-avg_marks')[:10]

# 3. Get students who haven't submitted a specific assignment
assignment = Assignment.objects.get(id=1)
not_submitted = Student.objects.filter(
    classroom=assignment.classroom
).exclude(
    submissions__assignment=assignment
)

# 4. Get teacher workload (number of assignments created)
teacher_workload = Teacher.objects.annotate(
    assignment_count=Count('created_assignments'),
    total_submissions=Count('created_assignments__submissions')
).order_by('-assignment_count')

# 5. Get class-wise attendance statistics
from django.db.models import Avg

class_attendance = ClassRoom.objects.annotate(
    student_count=Count('students'),
    avg_attendance=Avg(
        Case(
            When(
                students__attendance_records__status='present',
                then=1
            ),
            default=0,
            output_field=FloatField()
        ) * 100
    )
)
```

### Aggregations and Annotations

```python
# Subject-wise average marks
subject_performance = Result.objects.values('subject__name').annotate(
    avg_marks=Avg('marks'),
    max_marks=Max('marks'),
    min_marks=Min('marks'),
    student_count=Count('student', distinct=True)
).order_by('-avg_marks')

# Monthly attendance report
from django.db.models.functions import TruncMonth

monthly_attendance = Attendance.objects.annotate(
    month=TruncMonth('date')
).values('month').annotate(
    total=Count('id'),
    present=Count('id', filter=Q(status='present')),
    absent=Count('id', filter=Q(status='absent'))
).order_by('month')
```

---

## 5. Performance Optimization Tips

### Use select_related for foreign keys
```python
# Bad - causes N+1 queries
students = Student.objects.all()
for student in students:
    print(student.user.email)  # Each access hits DB

# Good - single query with JOIN
students = Student.objects.select_related('user', 'classroom').all()
for student in students:
    print(student.user.email)  # No extra DB hit
```

### Use prefetch_related for many-to-many
```python
# Bad
teachers = Teacher.objects.all()
for teacher in teachers:
    print(teacher.subjects.all())  # N+1 queries

# Good
teachers = Teacher.objects.prefetch_related('subjects').all()
for teacher in teachers:
    print(teacher.subjects.all())  # Prefetched
```

### Database Indexing
```python
# In models.py
class Student(models.Model):
    roll_no = models.CharField(max_length=30, unique=True, db_index=True)
    # ...
    
    class Meta:
        indexes = [
            models.Index(fields=['roll_no', 'classroom']),
            models.Index(fields=['is_active', 'admission_date']),
        ]
```

---

## 6. Backup and Restore

### SQLite
```bash
# Backup
cp db.sqlite3 backups/db_backup_$(date +%Y%m%d).sqlite3

# Restore
cp backups/db_backup_20240101.sqlite3 db.sqlite3
```

### MySQL
```bash
# Backup
mysqldump -u schooladmin -p smartschool_db > backup_$(date +%Y%m%d).sql

# Restore
mysql -u schooladmin -p smartschool_db < backup_20240101.sql
```

### MongoDB
```bash
# Backup
mongodump --db smartschool_db --out ./backups/mongo_backup_$(date +%Y%m%d)

# Restore
mongorestore --db smartschool_db ./backups/mongo_backup_20240101/smartschool_db
```

---

## 7. Troubleshooting

### MySQL Connection Issues
```python
# Check MySQL service is running
# Windows: services.msc -> MySQL
# Linux: sudo systemctl status mysql

# Test connection
mysql -u schooladmin -p smartschool_db
```

### Migration Issues
```bash
# Reset migrations (CAUTION: deletes all data)
python manage.py migrate school zero
python manage.py makemigrations
python manage.py migrate

# Fake migrations (if tables already exist)
python manage.py migrate --fake
```

### MongoDB Connection Issues
```bash
# Check MongoDB service
# Windows: services.msc -> MongoDB
# Linux: sudo systemctl status mongod

# Test connection
mongosh
use smartschool_db
db.stats()
```
