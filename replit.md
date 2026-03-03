# Django Certificate Management System

## Overview
A Django-based web application for managing certificates, users, and related workflows. Built with Django 5.2.2 and Python 3.11.

## Architecture
- **Framework**: Django 5.2.2
- **Python**: 3.11 (via `.pythonlibs`)
- **Database**: SQLite (`db2.sqlite3`)
- **Port**: 5000

## Key Apps
- `core` - Main Django project settings, URLs, WSGI/ASGI config, roles
- `login` - User authentication, registration, profile management
- `sn` - Core business logic (certificates, PDF generation, etc.)

## Environment Variables
- `DJANGO_SECRET_KEY` - Django secret key (stored in Replit secrets)
- `DJANGO_DEBUG` - Debug mode flag (default: True)

## Dependencies
- Django 5.2.2
- django-ckeditor 6.7.2
- django-role-permissions 3.2.0
- django-auth-ldap 5.2.0
- weasyprint (PDF generation)
- matplotlib, numpy, pillow (charts/images)
- python-ldap (LDAP authentication)
- gunicorn (production server)

## Running the App
The app runs via the "Start application" workflow:
```bash
python3.11 manage.py runserver 0.0.0.0:5000
```

## Static & Media Files
- Static files: `/static/` served from `staticfiles/`
- Media uploads: `/media/` served from `media/`
- CKEditor uploads go to `media/uploads/`

## Security Notes
- SECRET_KEY is stored as a Replit environment variable, not hardcoded
- DEBUG is controlled via environment variable
- ALLOWED_HOSTS is set to `['*']` for development - restrict in production
- CSRF trusted origins include Replit domains
