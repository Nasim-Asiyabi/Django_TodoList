📋 Django Reminder App - Task Management System

A comprehensive Django web application for managing tasks and reminders with advanced features including calendar integration, notifications, and custom Django model managers.

✨ Features
✅ Complete Task Management - Create, read, update, and delete tasks

✅ Custom Django Manager - Advanced filtering with expired_and_incomplete() method

✅ Multi-App Architecture - Separate apps for tasks, calendar, and notifications

✅ Responsive Design - Modern HTML/CSS interface

✅ Class-Based Views - Clean and maintainable code structure

✅ Template Inheritance - DRY principle implementation

✅ Django Admin - Built-in administration interface

✅ SQLite Database - Lightweight and easy to set up

📸 Screenshots
(Add your screenshots here)

<!-- | Task List | Create Task | Task Detail | |-----------|-------------|-------------| | ![Task List](screenshots/list.png) | ![Create Task](screenshots/create.png) | ![Task Detail](screenshots/detail.png) | -->
🏗️ Project Structure
text
django-reminder-app/
├── reminder/                  # Main project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # Main URL configuration
│   ├── asgi.py               # ASGI configuration
│   └── wsgi.py               # WSGI configuration
├── todo/                     # Core task management app
│   ├── migrations/           # Database migrations
│   ├── templates/todo/       # HTML templates
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── task_detail.html
│   │   ├── task_form.html
│   │   ├── task_status_form.html
│   │   └── task_confirm_delete.html
│   ├── __init__.py
│   ├── admin.py             # Admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Data models with custom Manager
│   ├── tests.py             # Unit tests
│   ├── urls.py              # App URL routing
│   └── views.py             # Class-Based Views
├── calender/                # Calendar integration app
├── notification/            # Notification system app
├── manage.py               # Django command-line utility
├── requirements.txt        # Python dependencies
├── LICENSE                 # MIT License
└── README.md              # This file
🚀 Quick Start
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation Steps
Clone the repository

bash
git clone https://github.com/yourusername/django-reminder-app.git
cd django-reminder-app
Create and activate virtual environment

bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
Apply database migrations

bash
python manage.py makemigrations
python manage.py migrate
Create superuser (optional)

bash
python manage.py createsuperuser
Run development server

bash
python manage.py runserver
Access the application

Open browser and go to: http://127.0.0.1:8000/todo/

Admin panel: http://127.0.0.1:8000/admin/

