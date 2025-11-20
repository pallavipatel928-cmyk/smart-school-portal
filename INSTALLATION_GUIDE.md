# Complete Installation & Usage Guide

## 📦 Installation Guide

### Method 1: Automated Setup (Recommended)

#### Windows (PowerShell):
```powershell
# Navigate to project directory
cd C:\Users\PALLAVI\OneDrive\Desktop\project2

# Run setup script
.\setup.ps1
```

#### Linux/macOS:
```bash
# Navigate to project directory
cd /path/to/project2

# Make script executable
chmod +x setup.sh

# Run setup script
./setup.sh
```

The script will:
- ✓ Check Python installation
- ✓ Create virtual environment
- ✓ Install dependencies
- ✓ Set up database
- ✓ Create directories
- ✓ Collect static files
- ✓ Prompt for admin account creation

---

### Method 2: Manual Setup

#### Step 1: Install Python
Download and install Python 3.10+ from https://www.python.org/downloads/

**Important:** Check "Add Python to PATH" during installation

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/macOS
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Configure Database
By default, SQLite is used (no configuration needed).

For MySQL or MongoDB, see `DATABASE_SETUP.md`

#### Step 5: Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

#### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

Enter:
- Username (e.g., admin)
- Email (e.g., admin@school.com)
- Password (minimum 8 characters)

#### Step 7: Start Server
```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## 🚀 First-Time Usage

### 1. Access Admin Panel
1. Go to http://127.0.0.1:8000/admin/
2. Login with superuser credentials
3. You'll see the Django admin interface

### 2. Create Initial Data

#### Create Subjects:
1. Click "Subjects" → "Add Subject"
2. Example subjects:
   - Name: Mathematics, Code: MATH101
   - Name: Physics, Code: PHY101
   - Name: Chemistry, Code: CHEM101
   - Name: English, Code: ENG101

#### Create Classrooms:
1. Click "Class Rooms" → "Add Class Room"
2. Examples:
   - Name: 10th Grade, Section: A
   - Name: 9th Grade, Section: B
   - Name: 11th Grade, Section: A

#### Create Teacher Users:
1. Click "Users" → "Add User"
2. Fill in:
   - Username: john_teacher
   - Password: (set password)
   - First name: John
   - Last name: Doe
   - Email: john@school.com
   - Role: Teacher
   - Staff status: ☑ (check)
   - Active: ☑ (check)
3. Click "Save"

#### Create Teacher Profile:
1. Click "Teachers" → "Add Teacher"
2. Select user: john_teacher
3. Fill in:
   - Subjects: (select subjects)
   - Qualification: M.Sc Mathematics
   - Experience years: 5
   - Is active: ☑
4. Click "Save"

#### Create Student Users:
1. Click "Users" → "Add User"
2. Fill in:
   - Username: jane_student
   - Password: (set password)
   - First name: Jane
   - Last name: Smith
   - Email: jane@school.com
   - Role: Student
   - Active: ☑
3. Click "Save"

#### Create Student Profile:
1. Click "Students" → "Add Student"
2. Select user: jane_student
3. Fill in:
   - Roll no: 2024001
   - Classroom: (select classroom)
   - Parent name: John Smith
   - Parent phone: 1234567890
   - Is active: ☑
4. Click "Save"

### 3. Test the System

#### Login as Teacher:
1. Logout from admin
2. Go to http://127.0.0.1:8000/login/
3. Login with: john_teacher / (password)
4. You'll see teacher dashboard

#### Create Assignment:
1. Click "Assignments" → "Create Assignment"
2. Fill in:
   - Title: Chapter 1 Exercise
   - Description: Complete all questions
   - Subject: Mathematics
   - Classroom: 10th Grade - A
   - Due date: (select future date)
   - Total marks: 100
3. Click "Create Assignment"

#### Mark Attendance:
1. Click "Attendance" → "Mark Attendance"
2. Select:
   - Student
   - Subject
   - Date
   - Status: Present/Absent/Leave
3. Click "Mark"

#### Login as Student:
1. Logout and login with: jane_student / (password)
2. View assignments, notices, results
3. Submit assignments

---

## 📖 Detailed Feature Usage

### For Administrators

#### User Management:
```
Admin Panel → Users
- View all users
- Activate/deactivate accounts
- Change user roles
- Reset passwords
```

#### System Configuration:
```
Admin Panel → Class Rooms / Subjects
- Add new classes
- Create subjects
- Assign class teachers
```

#### Reports:
Access Django admin to:
- View attendance statistics
- Check submission status
- Analyze student performance

---

### For Teachers

#### Create Assignments:
1. Dashboard → Assignments → Create Assignment
2. Fill required fields
3. Optional: Upload reference file
4. Set due date and marks

#### Mark Attendance:
1. Dashboard → Attendance → Mark Attendance
2. Select date and subject
3. Mark students as Present/Absent/Leave
4. Add remarks if needed

#### Enter Results:
1. Dashboard → Results → Add Result
2. Select student and subject
3. Enter marks and exam name
4. Grade is calculated automatically

#### Post Notices:
1. Dashboard → Notices → Create Notice
2. Write title and content
3. Select target audience (All/Teachers/Students)
4. Set publish and expiry dates

#### View Student Performance:
1. Dashboard → Students
2. Click on student name
3. View attendance, results, submissions

---

### For Students

#### View Assignments:
1. Dashboard → Assignments
2. See all assignments for your class
3. Check due dates
4. Download assignment files

#### Submit Assignments:
1. Click on assignment
2. Click "Submit"
3. Upload your file
4. Submission is marked with timestamp

#### Check Results:
1. Dashboard → Results
2. View all exam marks
3. See grades and percentages
4. Track performance over time

#### View Attendance:
1. Dashboard → Profile
2. See attendance percentage
3. View attendance history

#### Read Notices:
1. Dashboard → Notices
2. View all announcements
3. Filter by date

---

## 🔧 Common Tasks

### Add Bulk Students (Django Shell)
```python
python manage.py shell
```

```python
from school.models import User, Student, ClassRoom

classroom = ClassRoom.objects.get(name="10th Grade", section="A")

students_data = [
    ("student001", "Alice", "Johnson", "alice@school.com"),
    ("student002", "Bob", "Williams", "bob@school.com"),
    ("student003", "Charlie", "Brown", "charlie@school.com"),
]

for username, first_name, last_name, email in students_data:
    user = User.objects.create_user(
        username=username,
        email=email,
        password="defaultpass123",
        role="student",
        first_name=first_name,
        last_name=last_name,
        is_active=True
    )
    
    Student.objects.create(
        user=user,
        roll_no=username.upper(),
        classroom=classroom,
        is_active=True
    )

print("Students created successfully!")
```

### Export Data
```bash
# Export all data
python manage.py dumpdata > backup_full.json

# Export specific model
python manage.py dumpdata school.Student > students_backup.json

# Export with indentation
python manage.py dumpdata --indent 2 school > school_backup.json
```

### Import Data
```bash
python manage.py loaddata backup_full.json
```

### Reset Database (CAUTION: Deletes all data)
```bash
# Delete database
del db.sqlite3  # Windows
rm db.sqlite3   # Linux/macOS

# Recreate
python manage.py migrate
python manage.py createsuperuser
```

---

## 🌐 API Usage

### Authentication
First, login via web interface, then use session authentication for API calls.

### Get Students List
```bash
curl http://127.0.0.1:8000/api/students/ \
  -H "Cookie: sessionid=YOUR_SESSION_ID"
```

### Get Student Details
```bash
curl http://127.0.0.1:8000/api/students/1/
```

### Get Student Attendance
```bash
curl http://127.0.0.1:8000/api/students/1/attendance/
```

### Using Python requests:
```python
import requests

# Login first
session = requests.Session()
login_url = "http://127.0.0.1:8000/login/"
session.post(login_url, data={
    'username': 'admin',
    'password': 'yourpassword'
})

# Get data
response = session.get("http://127.0.0.1:8000/api/students/")
students = response.json()
print(students)
```

---

## 🎨 Customization Guide

### Change Color Scheme
Edit `static/css/style.css`:

```css
:root {
    --primary-color: #your-color;
    --secondary-color: #your-color;
    /* ... */
}
```

### Add Custom Pages
1. Create view in `school/views.py`
2. Create template in `templates/school/`
3. Add URL in `school/urls.py`

### Modify Models
1. Edit `school/models.py`
2. Run: `python manage.py makemigrations`
3. Run: `python manage.py migrate`

### Add New Features
Follow Django's MTV (Model-Template-View) pattern:
1. **Model**: Define data structure
2. **View**: Handle logic
3. **Template**: Display data
4. **URL**: Map URLs to views

---

## 📊 Sample Workflows

### Complete Assignment Workflow:
1. **Teacher** creates assignment
2. **Student** views assignment in dashboard
3. **Student** downloads assignment file (if any)
4. **Student** completes work and submits file
5. **Teacher** views submissions
6. **Teacher** grades submission and adds remarks
7. **Student** sees marks and feedback

### Attendance Workflow:
1. **Teacher** marks daily attendance
2. System calculates attendance percentage
3. **Student** views attendance in profile
4. **Admin** generates attendance reports

### Exam Results Workflow:
1. **Teacher/Admin** enters exam marks
2. System auto-calculates grades
3. **Student** views results in dashboard
4. System tracks performance trends

---

## 🔐 Security Best Practices

### For Development:
- Keep DEBUG = True
- Use development server
- SQLite is fine

### For Production:
1. Set DEBUG = False
2. Change SECRET_KEY
3. Configure ALLOWED_HOSTS
4. Use MySQL/PostgreSQL
5. Set up HTTPS
6. Use environment variables
7. Enable CSRF protection
8. Set secure cookies
9. Regular backups
10. Monitor logs

---

## 📞 Troubleshooting

### Server won't start:
```bash
# Check for port conflicts
python manage.py runserver 8080

# Check for errors
python manage.py check
```

### Static files not loading:
```bash
python manage.py collectstatic --clear
```

### Database errors:
```bash
# Check migrations
python manage.py showmigrations

# Migrate specific app
python manage.py migrate school
```

### Import errors:
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Learning Resources

- **Django Docs**: https://docs.djangoproject.com/
- **DRF Docs**: https://www.django-rest-framework.org/
- **Bootstrap**: https://getbootstrap.com/
- **Python**: https://docs.python.org/

---

## ✅ Checklist for Production

- [ ] DEBUG = False
- [ ] SECRET_KEY changed
- [ ] ALLOWED_HOSTS configured
- [ ] Database: MySQL/PostgreSQL
- [ ] Static files collected
- [ ] Media files served properly
- [ ] HTTPS enabled
- [ ] Email configured
- [ ] Backups scheduled
- [ ] Error logging setup
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Monitoring setup

---

**Happy Learning & Building! 🎓**
