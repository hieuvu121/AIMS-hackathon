# Django Backend

This is the Django REST API backend for the SmartCompliance AI platform.

## Features

- REST API endpoints for data management
- Database models for modern slavery compliance data
- Admin interface for data management
- API serializers and views
- Static file serving

## Getting Started

1. Navigate to this directory:
   ```bash
   cd project/django_backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run database migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser (optional):
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000`.

## Project Structure

```
├── light_carriers/     # Main Django project settings
├── main/              # Main application with models and views
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## API Endpoints

- Admin interface: `http://localhost:8000/admin/`
- API endpoints: `http://localhost:8000/api/`

## Database

The application uses SQLite by default. The database file `db.sqlite3` is included in the project.
