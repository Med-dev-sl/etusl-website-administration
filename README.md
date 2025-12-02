# ETUSL CMS - University Content Management System

A full-featured, modern CMS built with Django and Django REST Framework for managing university websites, news, events, and staff directories.

## MVP Features (Sprint 1)

- **User Authentication & Roles**: SuperAdmin, Web Editor, Faculty Editor
- **Dynamic Pages**: Create, edit, publish pages with rich-text editing
- **News & Announcements**: CRUD news with categories, featured pins, and expiry dates
- **Events & Calendar**: Manage events with RSVP support and calendar views
- **Staff Directory**: Searchable staff profiles with photos and contact info
- **Media Management**: Upload and manage images, videos, and documents
- **REST API**: Read-only API for news and events (extensible for mobile apps)
- **Admin Dashboard**: Django admin interface with custom views for all models

## Project Structure

```
admin_dashboard/
├── admin_dashboard/          # Project config (settings, urls, wsgi)
├── users/                    # User profiles & roles
├── pages/                    # Dynamic pages
├── news/                     # News & announcements
├── events/                   # Events & calendar
├── staff/                    # Staff directory
├── media/                    # Media management
├── manage.py
├── db.sqlite3               # Development database
└── migrations/              # Database migrations
```

## Setup & Installation

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)
- PostgreSQL (optional, SQLite for dev)

### Local Development

1. **Activate virtual environment:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # macOS/Linux
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations:**
   ```bash
   cd admin_dashboard
   python manage.py migrate
   ```

4. **Create superuser (if not already created):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Admin Panel: `http://localhost:8000/admin/`
   - News API: `http://localhost:8000/api/news/`
   - Login with credentials: `ETUSLWEB001` / `P@$$W0RD` (created during setup)

## API Endpoints

### News
- `GET /api/news/` - List all news posts
- `GET /api/news/{id}/` - Get single news post
- `POST /api/news/` - Create news post (admin only)
- `PUT /api/news/{id}/` - Update news post (admin only)
- `DELETE /api/news/{id}/` - Delete news post (admin only)

## Models Overview

### Users
- `Profile`: Extended user profile with biography

### Pages
- `Page`: Dynamic pages (About, Contact, etc.) with rich-text content

### News
- `NewsPost`: News articles with featured flag and publish date

### Events
- `Event`: Events with start/end times, location, and description

### Staff
- `StaffMember`: Staff profiles with department, title, email, and photo

### Media
- `MediaFile`: File uploads categorized as image, video, or document

## Environment Variables

Create a `.env` file in the project root:
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3

# Optional: For PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost:5432/etusl_cms

# Optional: For S3 storage
# AWS_ACCESS_KEY_ID=your-key
# AWS_SECRET_ACCESS_KEY=your-secret
# AWS_STORAGE_BUCKET_NAME=your-bucket
```

## Database Configuration

### Development (SQLite - Default)
No configuration needed. SQLite database is created automatically.

### Production (PostgreSQL)
Update `settings.py` `DATABASES` section:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'etusl_cms',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## Testing

Run tests (when added):
```bash
cd admin_dashboard
python manage.py test
```

## Deployment

### Using Docker

1. **Build image:**
   ```bash
   docker build -t etusl-cms .
   ```

2. **Run container:**
   ```bash
   docker run -p 8000:8000 etusl-cms
   ```

### Using Render/Heroku/DigitalOcean
See `DEPLOYMENT.md` (coming soon)

## Project Roadmap

### Sprint 1 (Current - Weeks 1-2)
- [x] Project scaffold
- [x] Core models & migrations
- [x] Admin interface setup
- [ ] Basic REST API
- [ ] Tests for models

### Sprint 2 (Weeks 3-4)
- Homepage builder (drag & drop)
- Multilingual support
- Form builder
- Advanced search

### Sprint 3+ (Weeks 5+)
- Student portal
- Alumni & testimonials
- Analytics dashboard
- Live chat integration

## Technology Stack

- **Backend**: Django 5.2+, Django REST Framework
- **Database**: PostgreSQL (production), SQLite (dev)
- **File Storage**: Local storage (dev), AWS S3 (production)
- **Frontend**: Django Templates (current), React.js (future)
- **Deployment**: Docker, Render, DigitalOcean, Heroku

## Contributing

Guidelines coming soon.

## License

TBD

## Contact

For questions or support, contact: ETUSL Web Development Team

---

**Last Updated**: December 2, 2025
**Version**: 0.1.0 (MVP)
