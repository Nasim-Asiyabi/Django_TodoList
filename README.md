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

