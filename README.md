# 🎓 Smart School Portal

A comprehensive, full-featured **School Management System** built with Django that digitizes and streamlines school administration, teaching, and learning processes.

![Django](https://img.shields.io/badge/Django-5.2.8-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## ✨ Features

### 👥 Multi-Role System
- **Students**: View assignments, check grades, track attendance
- **Teachers**: Manage assignments, mark attendance, grade students
- **Admin/Principal**: Full school oversight and management

### 📚 Core Modules
- ✅ Assignment Management
- ✅ Attendance Tracking
- ✅ Exam & Results System
- ✅ Notice Board
- ✅ Library Management
- ✅ Fee Management
- ✅ Timetable & Events
- ✅ Meeting Portal (Staff/Parent meetings)
- ✅ Internal Messaging System

### 🎨 Beautiful UI
- AI-generated illustrations
- Gradient-based modern design
- Responsive Bootstrap 5 layout
- Smooth animations and transitions
- Mobile-friendly interface

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/smart-school-portal.git
cd smart-school-portal
```

2. **Create virtual environment**
```bash
python -m venv venv
```

3. **Activate virtual environment**

Windows:
```bash
venv\Scripts\activate
```

Linux/Mac:
```bash
source venv/bin/activate
```

4. **Install dependencies**
```bash
pip install -r requirements.txt
```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Access the portal**
```
http://127.0.0.1:8000/
```

---

## 🔑 Demo Accounts

### Teachers
- **Pallavi Patel**: `teacher1` / `teacher123`
- **Gayathri**: `teacher2` / `teacher123`
- **Michael Brown**: `teacher3` / `teacher123`

### Admin Panel
Access at: `http://127.0.0.1:8000/admin/`

---

## 📁 Project Structure

```
smart-school-portal/
├── core/                   # Django project settings
├── school/                 # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── admin.py           # Admin configuration
│   └── forms.py           # Form definitions
├── templates/             # HTML templates
│   ├── school/           # App templates
│   └── admin/            # Admin templates
├── static/               # Static files (CSS, JS)
├── media/                # User uploads
├── requirements.txt      # Python dependencies
├── manage.py            # Django management script
└── README.md            # This file
```

---

## 🛠️ Technology Stack

**Backend:**
- Django 5.2.8
- Django REST Framework 3.14.0
- SQLite (default) / PostgreSQL (production)

**Frontend:**
- Bootstrap 5.3.0
- Font Awesome 6.4.0
- Custom CSS with animations

**Deployment:**
- Gunicorn
- WhiteNoise
- python-decouple

---

## 🌐 Deployment

### Deploy to Render (Free)

1. Push code to GitHub
2. Go to [Render](https://render.com)
3. Create new Web Service
4. Connect GitHub repository
5. Configure:
   - Build: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - Start: `gunicorn core.wsgi`
6. Add environment variables
7. Deploy!

See `DEPLOYMENT_GUIDE.md` for detailed instructions for multiple platforms.

---

## 📖 Documentation

- **Installation Guide**: `INSTALLATION_GUIDE.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **Quick Start**: `QUICKSTART.md`
- **Database Setup**: `DATABASE_SETUP.md`

---

## 🎯 Key Highlights

- **Modern Design**: Professional gradients and animations
- **User-Friendly**: Intuitive navigation
- **Scalable**: Handle multiple schools
- **Secure**: Industry-standard security
- **Mobile-Ready**: Works on all devices
- **Fast**: Optimized performance

---

## 📸 Screenshots

### Dashboard
Beautiful role-based dashboards with AI-generated illustrations

### Teacher Portal
- Teacher Profile Management
- Subject Directory
- Faculty List
- Student Interaction Hub
- Communication Center

### Meeting Portal
- Schedule meetings with staff/parents
- Virtual meeting support (Zoom/Google Meet)
- Meeting status tracking

### Admin Panel
- Feature boards with gradient designs
- Real-time statistics
- System management

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Pallavi Patel**

---

## 🙏 Acknowledgments

- Built with Django
- UI powered by Bootstrap
- Icons by Font Awesome

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Contact: [Your Email]

---

**Made with ❤️ for Smart Education Management**

🎓 Transforming education through technology!
