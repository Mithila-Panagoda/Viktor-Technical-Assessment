# Django REST Framework Template Server

A clean and simple Django REST Framework template server for quickly setting up Django DRF projects with PostgreSQL.

## Features

- Django REST Framework (DRF)
- JWT Authentication (Simple JWT)
- API Documentation (Swagger/Redoc via drf-yasg)
- CORS support
- PostgreSQL database support

## Prerequisites

- Python 3.8 or higher
- PostgreSQL database

## Quick Start

1. **Clone and navigate to the project:**
   ```bash
   cd server
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your `.env` file:**
   
   Create a `.env` file in the `server` directory with the following:
   ```env
   # Database Configuration (PostgreSQL)
   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PWD=your_database_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432

   # Environment
   ENVIRONMENT=development

   # Frontend URL
   WEBAPP_URL=http://localhost:3000

   # Swagger Documentation
   IS_SWAGGER_ENABLED=true
   SWAGGER_ADMIN_LOGIN_ENABLED=false
   ```

   > See `project/settings.py` for additional configuration options and environment variables.

5. **Set up the database:**
   
   The database configuration is loaded from environment variables in `project/settings.py`. Make sure your PostgreSQL database is running and create your database:
   ```bash
   # Using psql
   createdb your_database_name
   ```
   
   The template automatically configures the database connection using the following environment variables:
   - `DATABASE_NAME`: The name of your PostgreSQL database
   - `DATABASE_USER`: PostgreSQL username
   - `DATABASE_PWD`: PostgreSQL password
   - `DATABASE_HOST`: Database host (default: localhost)
   - `DATABASE_PORT`: Database port (default: 5432)

6. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

7. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

   The server will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI:** `http://localhost:8000/swagger/schema/`
- **Redoc:** `http://localhost:8000/redoc/`

## Project Structure

```
server/
├── apps/              # Django apps
├── project/           # Project settings (see settings.py for configuration)
│   ├── settings.py    # Django settings and environment variable usage
│   ├── urls.py        # Main URL configuration
│   └── ...
├── manage.py          # Django management script
├── requirements.txt   # Python dependencies
└── .env              # Environment variables (create this file)
```

## Database Configuration

The template uses PostgreSQL and loads database configuration from environment variables. The database settings are configured in `project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME', 'postgres'),
        'USER': os.environ.get('DATABASE_USER', 'postgres'),
        'PASSWORD': os.environ.get('DATABASE_PWD', 'postgres'),
        'HOST': os.environ.get('DATABASE_HOST', 'localhost'),
        'PORT': os.environ.get("DATABASE_PORT", '5432'),
    }
}
```

Make sure all database environment variables are set in your `.env` file before running migrations.

## Configuration

For detailed configuration options and other environment variables, refer to `project/settings.py`.


## License

This template is open source and available for use in your projects.
