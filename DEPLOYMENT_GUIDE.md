# 🚀 Smart School Portal - Deployment Guide

This guide will help you deploy your Smart School Management Portal to various platforms.

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Deploy to Render (Recommended - Free)](#deploy-to-render)
3. [Deploy to PythonAnywhere (Free Tier Available)](#deploy-to-pythonanywhere)
4. [Deploy to Heroku](#deploy-to-heroku)
5. [Deploy to Railway](#deploy-to-railway)
6. [Deploy to Your Own Server (VPS)](#deploy-to-vps)
7. [Post-Deployment Steps](#post-deployment-steps)

---

## ✅ Pre-Deployment Checklist

### 1. **Update Requirements**
Your `requirements.txt` is already updated with deployment packages:
```
Django==4.2.7
djangorestframework==3.14.0
Pillow==10.1.0
gunicorn==21.2.0
whitenoise==6.6.0
python-decouple==3.8
dj-database-url==2.1.0
psycopg2-binary==2.9.9
```

### 2. **Create Environment File**
Copy `.env.example` to `.env` and update values:
```bash
cp .env.example .env
```

### 3. **Generate Secret Key**
Run this in Python shell:
```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### 4. **Collect Static Files**
```bash
python manage.py collectstatic --noinput
```

### 5. **Run Migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. **Create Superuser**
```bash
python manage.py createsuperuser
```

---

## 🌐 Deploy to Render (Recommended - Free)

Render offers free hosting for web applications with automatic deployments from Git.

### Step 1: Push Code to GitHub

1. Initialize git (if not already):
```bash
git init
git add .
git commit -m "Initial commit - Smart School Portal"
```

2. Create a new repository on GitHub (https://github.com/new)

3. Push your code:
```bash
git remote add origin https://github.com/YOUR_USERNAME/smart-school-portal.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy on Render

1. Go to https://render.com and sign up/login
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure the service:

**Settings:**
- **Name**: `smart-school-portal`
- **Environment**: `Python 3`
- **Region**: Choose closest to you
- **Branch**: `main`
- **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
- **Start Command**: `gunicorn core.wsgi:application`
- **Plan**: Free

5. **Add Environment Variables:**
Click "Environment" → Add following variables:
```
SECRET_KEY=your-generated-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app-name.onrender.com
DATABASE_URL=(leave empty for SQLite, or add PostgreSQL URL)
```

6. Click "Create Web Service"

7. Wait for deployment (5-10 minutes first time)

8. Your app will be live at: `https://your-app-name.onrender.com`

### Step 3: Create Superuser on Render

1. Go to your service → "Shell" tab
2. Run:
```bash
python manage.py createsuperuser
```

---

## 🐍 Deploy to PythonAnywhere

PythonAnywhere offers free hosting with some limitations.

### Step 1: Sign Up

1. Go to https://www.pythonanywhere.com
2. Create a free account
3. Go to "Web" tab

### Step 2: Upload Your Code

**Option A: Using Git**
```bash
git clone https://github.com/YOUR_USERNAME/smart-school-portal.git
cd smart-school-portal
```

**Option B: Upload Manually**
1. Zip your project
2. Upload via "Files" tab
3. Extract the zip

### Step 3: Create Virtual Environment

```bash
cd /home/YOUR_USERNAME/smart-school-portal
mkvirtualenv --python=/usr/bin/python3.10 myenv
pip install -r requirements.txt
```

### Step 4: Configure Web App

1. Go to "Web" tab → "Add a new web app"
2. Choose "Manual configuration" → Python 3.10
3. Set paths:

**Source code**: `/home/YOUR_USERNAME/smart-school-portal`
**Working directory**: `/home/YOUR_USERNAME/smart-school-portal`
**Virtualenv**: `/home/YOUR_USERNAME/.virtualenvs/myenv`

**WSGI configuration file**: Edit and add:
```python
import sys
import os

path = '/home/YOUR_USERNAME/smart-school-portal'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 5: Setup Static Files

In Web tab, add static files mapping:
```
URL: /static/
Directory: /home/YOUR_USERNAME/smart-school-portal/staticfiles
```

### Step 6: Run Commands

In Bash console:
```bash
cd smart-school-portal
workon myenv
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Step 7: Reload Web App

Click "Reload" button on Web tab

Your app will be live at: `https://YOUR_USERNAME.pythonanywhere.com`

---

## 🚂 Deploy to Railway

Railway provides free tier with $5 credit per month.

### Step 1: Deploy from GitHub

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository

### Step 2: Add PostgreSQL (Optional)

1. Click "+ New" → "Database" → "Add PostgreSQL"
2. Railway will auto-set `DATABASE_URL`

### Step 3: Configure Environment Variables

Add in Variables tab:
```
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=*.up.railway.app
```

### Step 4: Configure Build & Deploy

Railway auto-detects Django, but verify:
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `gunicorn core.wsgi`

### Step 5: Run Migrations

In Railway dashboard:
1. Go to your service
2. Click "..." → "Run Command"
3. Run:
```bash
python manage.py migrate
python manage.py createsuperuser
```

Your app will be live at: `https://your-app.up.railway.app`

---

## ☁️ Deploy to Heroku

### Step 1: Install Heroku CLI

Download from: https://devcenter.heroku.com/articles/heroku-cli

### Step 2: Login and Create App

```bash
heroku login
heroku create smart-school-portal
```

### Step 3: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:mini
```

### Step 4: Set Environment Variables

```bash
heroku config:set SECRET_KEY="your-secret-key-here"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
```

### Step 5: Deploy

```bash
git push heroku main
```

### Step 6: Run Migrations

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
heroku run python manage.py collectstatic --noinput
```

Your app will be live at: `https://smart-school-portal.herokuapp.com`

---

## 🖥️ Deploy to VPS (Ubuntu Server)

### Step 1: Setup Server

```bash
sudo apt update
sudo apt upgrade -y
sudo apt install python3-pip python3-dev libpq-dev nginx curl -y
```

### Step 2: Clone Your Code

```bash
cd /var/www
sudo git clone https://github.com/YOUR_USERNAME/smart-school-portal.git
cd smart-school-portal
```

### Step 3: Create Virtual Environment

```bash
sudo python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Configure Environment

```bash
sudo nano .env
```
Add your environment variables.

### Step 5: Setup Gunicorn

Create systemd service:
```bash
sudo nano /etc/systemd/system/smartschool.service
```

Add:
```ini
[Unit]
Description=Smart School Portal
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/smart-school-portal
Environment="PATH=/var/www/smart-school-portal/venv/bin"
ExecStart=/var/www/smart-school-portal/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 core.wsgi:application

[Install]
WantedBy=multi-user.target
```

Start service:
```bash
sudo systemctl start smartschool
sudo systemctl enable smartschool
```

### Step 6: Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/smartschool
```

Add:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/smart-school-portal/staticfiles/;
    }

    location /media/ {
        alias /var/www/smart-school-portal/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/smartschool /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

### Step 7: Setup SSL (Optional but Recommended)

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your_domain.com
```

---

## 🔧 Post-Deployment Steps

### 1. **Verify Deployment**
- Access your app URL
- Login to admin panel: `/admin/`
- Test main features:
  - Dashboard
  - Teacher Portal
  - Student Portal
  - Meeting Portal
  - Messaging System

### 2. **Create Initial Data**

Run in your deployment platform's shell:
```bash
python manage.py shell
```

Then:
```python
from school.models import User, Teacher, Student, ClassRoom, Subject

# Create sample classroom
classroom = ClassRoom.objects.create(name="Class 10A", section="A", class_teacher=None)

# Create sample subjects
math = Subject.objects.create(name="Mathematics", code="MATH101", description="Math subject")
science = Subject.objects.create(name="Science", code="SCI101", description="Science subject")
```

### 3. **Setup Teachers**
Use the teacher creation script we created earlier:
- Login as admin
- Go to `/admin/school/teacher/`
- Add teachers

### 4. **Enable Email (Optional)**

Update `.env` or environment variables:
```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 5. **Monitor Logs**

**Render**: Dashboard → Logs tab
**Railway**: Dashboard → Deployments → View Logs
**Heroku**: `heroku logs --tail`
**VPS**: `sudo journalctl -u smartschool -f`

### 6. **Backup Database**

**SQLite** (Local):
```bash
cp db.sqlite3 db.backup.sqlite3
```

**PostgreSQL** (Production):
```bash
# Heroku
heroku pg:backups:capture
heroku pg:backups:download

# VPS
pg_dump dbname > backup.sql
```

---

## 🔒 Security Checklist

- ✅ Set `DEBUG=False` in production
- ✅ Use strong `SECRET_KEY`
- ✅ Set `ALLOWED_HOSTS` correctly
- ✅ Enable HTTPS/SSL
- ✅ Use environment variables for sensitive data
- ✅ Regular database backups
- ✅ Keep dependencies updated
- ✅ Enable CSRF protection (already enabled)
- ✅ Set secure cookie flags in production

---

## 📞 Support

If you face any issues:

1. Check deployment platform logs
2. Verify environment variables
3. Ensure migrations are run
4. Check static files are collected
5. Verify database connection

---

## 🎉 Congratulations!

Your Smart School Portal is now live! 🚀

Access your app and start managing your school digitally! 🎓

**Features Available:**
- ✅ Student Portal
- ✅ Teacher Portal with AI illustrations
- ✅ Admin Panel with beautiful boards
- ✅ Meeting Portal for scheduling
- ✅ Messaging System
- ✅ Attendance Management
- ✅ Assignment Tracking
- ✅ Notice Board
- ✅ Library Management
- ✅ And much more!

---

**Made with ❤️ for Smart Education Management**
