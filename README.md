# Fashion Backend API

Django REST API backend for serving fashion images and team member data.

## Features

- REST API endpoints for team member data
- Image serving from backend
- CORS enabled for frontend integration
- Database models for team members and images

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Populate database with images:
```bash
python manage.py populate_data
```

4. Start development server:
```bash
python manage.py runserver
```

## API Endpoints

- `GET /api/card-data/` - Get all team member data with images
- `GET /api/team-members/` - Get team members list
- `GET /images/<image_name>` - Serve individual images

## Database Models

- **TeamMember**: Stores team member information
- **FashionImage**: Stores image files and metadata

## CORS Configuration

CORS is configured to allow requests from:
- http://localhost:3000 (React development server)
- http://127.0.0.1:3000

For production, update CORS_ALLOWED_ORIGINS in settings.py
