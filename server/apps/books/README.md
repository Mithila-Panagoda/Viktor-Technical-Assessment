# Books App 📚

The Books app is a comprehensive book catalog management system that provides a RESTful API for managing book inventory. Think of it as your digital library backend—it handles everything from storing book metadata to providing powerful search and filtering capabilities.

## 🎯 What This App Does

At its core, this app manages books. But it's designed to do more than just store data—it makes finding and organizing books incredibly easy through advanced filtering, sorting, and search capabilities. Whether you're building an online bookstore, a library management system, or a book recommendation platform, this app provides the foundation.

## 📊 The Book Model

Every book in the system has the following information:

- **Name**: The title of the book
- **Author**: Who wrote it
- **Publisher**: The publishing company
- **Publication Date**: When it was published
- **ISBN**: Unique identifier (13 digits, unique across all books)
- **Cover Photo**: An optional image file

This simple but complete structure gives you everything you need to build a book catalog.

## 🔍 Powerful Search & Filtering

One of the standout features of this app is how easy it makes finding books. The API supports:

### Single Field Filtering
Want all books by a specific author? Just add `?author=John%20Doe` to your request.

### Multiple Field Filtering
Need books from a specific publisher published in 2024? Combine filters: `?publisher=Penguin&publication_date=2024-01-01`

### Full-Text Search
Not sure which field contains what you're looking for? Use the search parameter to search across name, author, publisher, and ISBN simultaneously: `?search=python`

### Flexible Sorting
Sort by any field, ascending or descending, and combine multiple sort criteria:
- Single field: `?ordering=name` (ascending) or `?ordering=-name` (descending)
- Multiple fields: `?ordering=author,-publication_date` (author ascending, then publication date descending)

### Pagination
All results are paginated (20 items per page by default), so you never get overwhelmed with huge result sets.

## 🛠️ API Endpoints

All endpoints require authentication via JWT token.

### List Books
```
GET /api/books/
```
Returns paginated list of books with optional filtering, sorting, and search.

**Query Parameters:**
- `page`: Page number (default: 1)
- `name`: Filter by book name
- `author`: Filter by author name
- `publisher`: Filter by publisher
- `publication_date`: Filter by date (YYYY-MM-DD format)
- `isbn`: Filter by ISBN
- `search`: Search across name, author, publisher, ISBN
- `ordering`: Sort field(s) (prefix with `-` for descending)

**Example:**
```bash
# Get all books
GET /api/books/

# Get books by a specific author, sorted by publication date (newest first)
GET /api/books/?author=Stephen%20King&ordering=-publication_date

# Search for books containing "python" in any field
GET /api/books/?search=python

# Get page 2 of results
GET /api/books/?page=2
```

### Create Book
```
POST /api/books/
```
Create a new book entry.

**Request Body:**
```json
{
    "name": "Python Programming",
    "author": "John Doe",
    "publisher": "Tech Books Inc",
    "publication_date": "2024-01-15",
    "isbn": "9781234567890",
    "cover_photo": null
}
```

### Retrieve Book
```
GET /api/books/{id}/
```
Get details of a specific book.

### Update Book
```
PUT /api/books/{id}/
PATCH /api/books/{id}/
```
Update a book (full or partial update).

### Delete Book
```
DELETE /api/books/{id}/
```
Remove a book from the catalog.

## 💻 Code Structure

### Models (`models.py`)
The `Book` model defines the database structure with proper field types and constraints:
- String fields for text data
- Date field for publication date
- Unique constraint on ISBN to prevent duplicates
- Optional file field for cover photos

### Serializers (`serializers.py`)
The `BookSerializer` handles converting between Python objects and JSON:
- Includes all fields by default
- Handles file uploads for cover photos
- Validates data before saving

### Views (`views.py`)
The `BookViewSet` provides all CRUD operations:
- Built-in filtering and pagination
- Search functionality
- Sorting capabilities
- Standard REST actions

### URLs (`urls.py`)
Routes API requests to the appropriate viewset actions.

## 🎨 Django Admin Integration

Books are fully integrated into Django admin, allowing administrators to:
- View all books in a list
- Filter by author
- Search by book name
- Add, edit, and delete books through the web interface

## 🧪 Example Usage

### Creating a Book via API
```python
import requests

token = "your_jwt_token"
headers = {"Authorization": f"Bearer {token}"}

book_data = {
    "name": "Clean Code",
    "author": "Robert C. Martin",
    "publisher": "Prentice Hall",
    "publication_date": "2008-08-01",
    "isbn": "9780132350884"
}

response = requests.post(
    "http://localhost:8000/api/books/",
    json=book_data,
    headers=headers
)
```

### Filtering Books
```python
# Get books by a specific author
books = requests.get(
    "http://localhost:8000/api/books/?author=Robert%20C.%20Martin",
    headers=headers
).json()

# Search for books
results = requests.get(
    "http://localhost:8000/api/books/?search=code",
    headers=headers
).json()
```

## 🎓 Why This Design?

We chose this approach because:

1. **Flexibility**: The filtering system works for any use case—simple searches or complex queries
2. **Performance**: Pagination ensures fast responses even with large catalogs
3. **User Experience**: Multiple ways to find books (filter, search, sort) means users can always find what they need
4. **Standards**: Following REST principles makes the API intuitive for developers

## 🔗 Integration with Store App

Books created in this app can be added to shopping carts in the Store app. The ISBN and other metadata help identify books uniquely across the platform.

## 📈 Future Enhancements

Potential improvements could include:
- Book categories/genres
- Reviews and ratings
- Inventory tracking (stock levels)
- Book recommendations based on reading history
- Multi-language support
- Advanced analytics (popular books, trending authors)

## 🛡️ Security & Validation

- All endpoints require authentication
- ISBN uniqueness is enforced at the database level
- File uploads are validated for security
- All input is sanitized and validated

---

*Built with Django REST Framework - Making book management simple and powerful* 📖

