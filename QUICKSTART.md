# 🚀 Quick Start Guide - 5 Minutes to Running!

## Prerequisites Check
- ✅ Python installed? Check with: `python --version`
- ✅ Project downloaded? You should be in the project2 folder

---

## Windows Users (PowerShell)

### Option 1: Automated Setup (Easiest!)
```powershell
# Just run this one command:
.\setup.ps1
```

### Option 2: Manual Setup (If script doesn't work)
```powershell
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
.\venv\Scripts\Activate.ps1

# 3. Install packages
pip install Django djangorestframework pillow

# 4. Setup database
python manage.py migrate

# 5. Create admin account
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

---

## Linux/macOS Users

### Option 1: Automated Setup (Easiest!)
```bash
# Make script executable and run:
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup
```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install packages
pip install Django djangorestframework pillow

# 4. Setup database
python manage.py migrate

# 5. Create admin account
python manage.py createsuperuser

# 6. Start server
python manage.py runserver
```

---

## ⚡ Super Quick Start (Minimum Steps)

If you just want to see it running:

```bash
# 1. Install Django
pip install Django

# 2. Run migrations
python manage.py migrate

# 3. Create admin (username: admin, password: admin123)
python manage.py createsuperuser

# 4. Start server
python manage.py runserver
```

**Done!** Visit http://127.0.0.1:8000/

---

## 🎯 What to Do After Setup

### 1. Open Your Browser
Go to: http://127.0.0.1:8000/

### 2. Login to Admin Panel
Go to: http://127.0.0.1:8000/admin/
- Username: (what you created)
- Password: (what you created)

### 3. Add Sample Data (Recommended)

#### Create a Subject:
1. Click "Subjects" → "Add Subject"
2. Name: `Mathematics`, Code: `MATH101`
3. Save

#### Create a Classroom:
1. Click "Class Rooms" → "Add Class Room"
2. Name: `10th Grade`, Section: `A`
3. Save

#### Create a Teacher:
1. Click "Users" → "Add User"
2. Username: `teacher1`
3. Password: `teacher123`
4. Role: `Teacher`
5. Check "Staff status" and "Active"
6. Save

7. Click "Teachers" → "Add Teacher"
8. Select User: `teacher1`
9. Select Subjects: `Mathematics`
10. Save

#### Create a Student:
1. Click "Users" → "Add User"
2. Username: `student1`
3. Password: `student123`
4. Role: `Student`
5. Check "Active"
6. Save

7. Click "Students" → "Add Student"
8. Select User: `student1`
9. Roll No: `2024001`
10. Select Classroom: `10th Grade - A`
11. Save

### 4. Test the System

#### Login as Teacher:
1. Logout from admin
2. Go to http://127.0.0.1:8000/login/
3. Username: `teacher1`, Password: `teacher123`
4. Create an assignment!

#### Login as Student:
1. Logout
2. Login with: `student1` / `student123`
3. View assignments!

---

## 🛠️ Troubleshooting

### "Python not found"
**Solution:** Install Python from https://www.python.org/downloads/
Make sure to check "Add Python to PATH" during installation!

### "No module named django"
**Solution:** 
```bash
pip install Django
```

### "Port already in use"
**Solution:**
```bash
python manage.py runserver 8080
```
Then visit: http://127.0.0.1:8080/

### "Can't activate virtual environment on Windows"
**Solution:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

### "ImportError" or "Module not found"
**Solution:**
```bash
# Make sure virtual environment is activated!
# You should see (venv) in your terminal

# Then reinstall:
pip install -r requirements.txt
```

---

## 📱 Quick Commands Reference

```bash
# Start server
python manage.py runserver

# Create admin
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic
```

---

## 🎓 Next Steps

1. ✅ Read `README.md` for complete documentation
2. ✅ Check `DATABASE_SETUP.md` for MySQL/MongoDB setup
3. ✅ Read `INSTALLATION_GUIDE.md` for detailed usage
4. ✅ Explore the admin panel
5. ✅ Customize the system for your needs!

---

## 💡 Pro Tips

- **Bookmark the admin panel:** http://127.0.0.1:8000/admin/
- **Always activate virtual environment** before working
- **Use Django shell** for bulk operations
- **Read error messages carefully** - they're helpful!
- **Check the logs** in terminal for debugging

---

## 🎉 You're All Set!

The system is now running. Start exploring!

- **Home:** http://127.0.0.1:8000/
- **Admin:** http://127.0.0.1:8000/admin/
- **API:** http://127.0.0.1:8000/api/

**Need help?** Check the full documentation in README.md

---

**Have fun building! 🚀**
