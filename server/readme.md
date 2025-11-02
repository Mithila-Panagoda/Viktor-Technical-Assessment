# Django REST Framework Server

Welcome to the Viktor server! This is a production-ready Django REST Framework backend that powers an e-commerce platform. Whether you're setting this up for the first time or diving into the codebase, this guide will help you get started.

## 🌟 What This Server Does

This Django server provides a robust API backend for managing:
- **Books**: A complete book catalog with advanced search and filtering
- **Store Operations**: Shopping carts, product management, and intelligent recommendations
- **User Management**: Authentication, authorization, and user profiles

All built with Django REST Framework, following RESTful principles and industry best practices.

## ✨ Key Features

- 🔐 **JWT Authentication**: Secure token-based authentication using Simple JWT
- 📚 **Interactive API Docs**: Swagger UI and ReDoc documentation
- 🔍 **Advanced Filtering**: Multi-field filtering and sorting capabilities
- 🛒 **Shopping Cart System**: Flexible cart management with automatic calculations
- 🎯 **Recommendation Engine**: Smart product recommendations based on user behavior
- 🔒 **CORS Support**: Ready for frontend integration
- 🐘 **PostgreSQL**: Production-grade database support

## 🚀 Getting Started

### Prerequisites

Before you begin, make sure you have:
- **Python 3.8+** installed
- **PostgreSQL** database server running
- Basic familiarity with command line tools

### Step-by-Step Setup

1. **Navigate to the server directory:**
   ```bash
   cd server
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
   
   You should see `(venv)` in your terminal prompt, indicating the virtual environment is active.

3. **Install all dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   This installs Django, DRF, JWT authentication, database drivers, and all other required packages.

4. **Configure your environment:**
   
   Create a `.env` file in the `server` directory. This file stores sensitive configuration that shouldn't be committed to version control:
   
   ```env
   # Database Configuration (PostgreSQL)
   DATABASE_NAME=viktor_db
   DATABASE_USER=your_username
   DATABASE_PWD=your_password
   DATABASE_HOST=localhost
   DATABASE_PORT=5432
   
   # Environment
   ENVIRONMENT=development
   
   # Frontend URL (for CORS)
   WEBAPP_URL=http://localhost:3000
   
   # Swagger Documentation
   IS_SWAGGER_ENABLED=true
   SWAGGER_ADMIN_LOGIN_ENABLED=false
   
   # JWT Configuration (optional)
   SIMPLE_JWT_ACCESS_TOKEN_LIFETIME=5
   SIMPLE_JWT_REFRESH_TOKEN_LIFETIME=30
   ```
   
   > 💡 **Tip**: Never commit your `.env` file to git! It contains sensitive information.

5. **Create your PostgreSQL database:**
   
   Make sure PostgreSQL is running, then create the database:
   ```bash
   # Using psql command line
   createdb viktor_db
   
   # Or using PostgreSQL client
   psql -U your_username -c "CREATE DATABASE viktor_db;"
   ```

6. **Run database migrations:**
   ```bash
   python manage.py migrate
   ```
   
   This creates all the necessary database tables for users, books, shopping carts, and more.

7. **Create a superuser account:**
   ```bash
   python manage.py createsuperuser
   ```
   
   Follow the prompts to create an admin account. You'll use this to access the Django admin panel.

8. **Start the development server:**
   ```bash
   python manage.py runserver
   ```
   
   You should see output like:
   ```
   Starting development server at http://127.0.0.1:8000/
   Quit the server with CONTROL-C.
   ```

## 📚 Exploring the API

Once your server is running, you can explore the API in several ways:

### 1. Swagger UI (Interactive Documentation)
Visit: **http://localhost:8000/swagger/schema/**

This provides an interactive interface where you can:
- See all available endpoints
- Test API calls directly in the browser
- View request/response schemas
- Authenticate and make real API requests

### 2. ReDoc (Beautiful Documentation)
Visit: **http://localhost:8000/redoc/**

A beautifully formatted, static documentation view that's great for understanding the API structure at a glance.

### 3. Django Admin Panel
Visit: **http://localhost:8000/admin/**

Use the superuser credentials you created to access the admin interface. Here you can:
- Manage books, products, and shopping carts
- View user accounts
- Access all database models through a user-friendly interface

## 🏗️ Project Structure

Understanding the structure will help you navigate the codebase:

```
server/
├── apps/                      # Django applications
│   ├── books/                 # Book catalog management
│   │   ├── models.py          # Book data models
│   │   ├── views.py           # API endpoints
│   │   ├── serializers.py     # Data serialization
│   │   └── urls.py            # URL routing
│   ├── store/                 # Store and shopping cart system
│   │   ├── models.py          # Shopping cart models
│   │   ├── views.py           # Cart API endpoints
│   │   ├── serializers.py     # Cart serializers
│   │   ├── services.py        # Business logic layer
│   │   └── admin.py           # Django admin configuration
│   └── users/                 # User management
│       ├── models.py          # User model
│       ├── views.py           # Authentication endpoints
│       └── serializers.py     # User serializers
├── project/                   # Django project configuration
│   ├── settings.py            # All Django settings
│   ├── urls.py                # Main URL routing
│   └── swagger_config.py      # API documentation config
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
└── .env                       # Environment variables (create this)
```

## 🔧 Configuration Deep Dive

### Database Settings

The server uses PostgreSQL and configures the connection automatically from environment variables:

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

### REST Framework Settings

The API is configured with:
- **Pagination**: 20 items per page by default
- **Filtering**: Django-filter integration for advanced queries
- **Authentication**: JWT tokens for secure access
- **Permissions**: Authenticated users required by default

### Environment Variables

All configuration is environment-driven. Check `project/settings.py` for all available options, including:
- Database settings
- JWT token lifetimes
- CORS configuration
- Static file storage
- Email settings (commented out, ready to configure)

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication. Here's how it works:

1. **Login**: POST to `/api/users/login/` with email and password
2. **Receive Tokens**: Get access and refresh tokens
3. **Use Token**: Include token in Authorization header: `Bearer <access_token>`
4. **Refresh**: Use refresh token to get a new access token when it expires

Example:
```bash
# Login
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password123"}'

# Use token
curl http://localhost:8000/api/books/ \
  -H "Authorization: Bearer <your_access_token>"
```

## 📱 API Endpoints Overview

### Books API (`/api/books/`)
- List books with pagination, filtering, and sorting
- Create, retrieve, update, and delete books
- Search across multiple fields

### Store API (`/api/carts/`)
- Manage shopping carts
- Add/remove products
- Get cart totals
- Product recommendations

### Users API (`/api/users/`)
- User authentication (login)
- User profile management

## 🧪 Development Tips

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
After modifying models:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Django Shell
Explore the database interactively:
```bash
python manage.py shell
```

### Accessing the Database
```bash
python manage.py dbshell
```

## 🐛 Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `pg_isready`
- Check your `.env` file has correct credentials
- Ensure the database exists: `psql -l` to list databases

### Migration Issues
- If migrations fail, try: `python manage.py migrate --run-syncdb`
- For a fresh start: Delete migration files (except `__init__.py`) and re-run `makemigrations`

### Import Errors
- Ensure your virtual environment is activated
- Verify all dependencies are installed: `pip list`
- Check that you're in the correct directory

### Port Already in Use
If port 8000 is busy:
```bash
python manage.py runserver 8001
```

## 🚀 Next Steps

Now that you have the server running:

1. **Explore the Apps**: Check out the detailed documentation:
   - [Books App README](apps/books/README.md)
   - [Store App README](apps/store/README.md)

2. **Try the API**: Use Swagger UI to test endpoints

3. **Explore the Admin**: Log into Django admin and create some test data

4. **Read the Code**: The codebase is well-commented and follows Django best practices

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 💡 Design Philosophy

This server is built with several principles in mind:

- **Separation of Concerns**: Business logic in services, HTTP handling in views
- **Reusability**: Models and utilities can be used across apps
- **Maintainability**: Clear structure, helpful comments, comprehensive documentation
- **Scalability**: Patterns that work for both small and large applications

---

Happy coding! 🎉
