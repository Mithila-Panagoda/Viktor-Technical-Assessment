## 🏗️ Architecture Overview

The project follows a clean, modular architecture:

- **Books App**: A dedicated module for managing book inventory with advanced filtering and sorting
- **Store App**: A flexible e-commerce system supporting multiple product types with intelligent shopping cart management
- **Users App**: User management and authentication

Each app is self-contained with its own models, views, serializers, and business logic, making the codebase maintainable and scalable.

## 📚 Key Features

### Books Management
- Comprehensive book catalog with metadata (author, publisher, ISBN, publication date)
- Advanced API with pagination, filtering, and multi-field sorting
- RESTful endpoints for all CRUD operations

### Store System
- Multi-product type support (Books, Music Albums, Software Licenses)
- Intelligent shopping cart with automatic price/weight calculations
- Beautiful Django admin interface for cart management
- REST API for cart operations

### Recommendation Engine
- Data-driven product recommendations based on shopping patterns
- Analyzes product sequences to suggest what customers typically buy together
- Service layer architecture for clean business logic separation

## 🚀 Quick Start

```bash
# Navigate to the server directory
cd server

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment (see server/readme.md for details)
# Create .env file with database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start server
python manage.py runserver
```

Visit `http://localhost:8000` and explore the API documentation at `http://localhost:8000/swagger/schema/`

## 📖 Documentation

We've organized our documentation to make it easy to understand each component:

- **[Server Setup Guide](server/readme.md)** - Detailed setup instructions, configuration, and project structure
- **[Books App Documentation](server/apps/books/README.md)** - Everything about the book management system
- **[Store App Documentation](server/apps/store/README.md)** - Complete guide to the shopping cart and store functionality

## 🛠️ Technology Stack

- **Backend Framework**: Django 4.2 with Django REST Framework
- **Database**: PostgreSQL
- **Authentication**: JWT (JSON Web Tokens)
- **API Documentation**: Swagger/OpenAPI via drf-yasg
- **Architecture**: RESTful API with service layer pattern

## 🎯 Project Goals

This project demonstrates:

- **Clean Architecture**: Separation of concerns with models, views, serializers, and services
- **Scalability**: Design patterns that work for both small and large-scale applications
- **Developer Experience**: Intuitive APIs, comprehensive documentation, and helpful error messages
- **Production-Ready Features**: Authentication, filtering, pagination, and data validation

## 🤝 Getting Involved

Whether you're reviewing this for an interview, contributing to the project, or learning Django REST Framework, we hope you find the codebase clear and well-structured. Each component is designed to be self-explanatory, with comments and documentation where helpful.

## 📝 License

This project is open source and available for learning and development purposes.

---

*Built with ❤️ using Django REST Framework*

