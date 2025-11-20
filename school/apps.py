from django.apps import AppConfig


class SchoolConfig(AppConfig):
    """
    Configuration for the School app.
    
    This app handles all school management functionality including:
    - User management (Students, Teachers, Admin)
    - Academic features (Assignments, Results, Attendance)
    - Communication (Notices, Announcements)
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'school'
    verbose_name = 'School Management'
