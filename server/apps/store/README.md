# Store App 🛒

The Store app is the heart of our e-commerce platform. It's a flexible, intelligent shopping cart system that handles multiple product types (books, music albums, and software licenses) and includes a recommendation engine that learns from customer behavior. Think of it as your digital storefront's brain—it remembers what customers like, calculates totals automatically, and makes smart suggestions.

## 🎯 What Makes This App Special

Unlike simple cart systems, this one is built to handle real-world complexity. It can:
- Manage different types of products through a unified interface
- Automatically calculate prices and weights
- Learn from shopping patterns to provide recommendations
- Provide both a beautiful admin interface and a robust REST API

## 🏗️ Architecture Overview

The app follows a clean architecture pattern with clear separation of concerns:

- **Models**: Define the data structure (ShoppingCart, ShoppingCartItem, Product types)
- **Views**: Handle HTTP requests and responses
- **Serializers**: Convert data between Python objects and JSON
- **Services**: Business logic lives here (recommendations, calculations)
- **Admin**: Beautiful Django admin interface for management

This structure makes the code maintainable, testable, and easy to understand.

## 📦 Product Types

The store supports three types of products, each with its own characteristics:

### Books 📚
- Title, author, number of pages
- Price and weight for shipping calculations
- Linked to the Books app

### Music Albums 🎵
- Artist, number of tracks
- Price and weight
- Perfect for physical media or digital licenses

### Software Licenses 💿
- License-based products
- Price and weight (typically 0kg for digital)
- Flexible for SaaS and digital products

All products share common attributes (price, weight) which makes the cart system work seamlessly across types.

## 🛒 Shopping Cart System

### The ShoppingCart Model

Each cart is a container that:
- Belongs to a user (optional, for guest checkout support)
- Tracks creation and update timestamps
- Provides methods to add/remove products
- Automatically calculates totals

**Key Methods:**
- `add_product(product, quantity)`: Add a product (increments quantity if already in cart)
- `remove_product(product, quantity)`: Remove products (partial or complete)
- `calculate_total_price()`: Sum of all items (quantity × price)
- `calculate_total_weight()`: Sum of all items (quantity × weight)

### The ShoppingCartItem Model

Each item in a cart represents:
- A specific product (using Django's ContentType for flexibility)
- Quantity of that product
- Cached price and weight (optimized for fast calculations)
- Timestamp of when it was added

**Why Cached Price/Weight?**
When a product's price changes, we preserve what the customer saw at checkout time. The cached values ensure historical accuracy and fair pricing.

## 🔌 REST API Endpoints

All endpoints require JWT authentication.

### Cart Management

#### List Your Carts
```
GET /api/carts/
```
Returns all shopping carts for the authenticated user.

#### Create a Cart
```
POST /api/carts/
```
Creates a new shopping cart (automatically assigned to the user).

#### Get Cart Details
```
GET /api/carts/{id}/
```
Returns a cart with all its items, totals, and metadata.

#### Get or Create Your Active Cart
```
GET /api/carts/my-cart/
```
Convenience endpoint that returns your current cart or creates one if you don't have one.

#### Clear Cart
```
DELETE /api/carts/{id}/clear/
```
Removes all items from a cart.

### Product Operations

#### Add Product to Cart
```
POST /api/carts/{id}/add-product/
```

**Request Body:**
```json
{
    "product_type": "book",
    "product_id": "uuid-here",
    "quantity": 2
}
```

**Response:**
```json
{
    "message": "Product added to cart successfully",
    "cart": {
        "id": "cart-uuid",
        "items": [...],
        "total_price": "59.98",
        "total_weight": "1.00"
    }
}
```

#### Remove Product from Cart
```
POST /api/carts/{id}/remove-product/
```

**Request Body:**
```json
{
    "product_type": "book",
    "product_id": "uuid-here",
    "quantity": 1
}
```

#### Get Cart Totals
```
GET /api/carts/{id}/totals/
```

**Response:**
```json
{
    "cart_id": "cart-uuid",
    "total_price": "59.98",
    "total_weight": "1.00",
    "item_count": 2
}
```

### Product Recommendations

#### Get Recommendations
```
GET /api/carts/recommendations/
```

This is where the magic happens! Analyzes shopping patterns to suggest products.

**Query Parameters:**
- `user_id` (optional): Filter by specific user's carts
- `all_users` (optional): Analyze all carts (admin only)

**Response:**
```json
{
    "recommendations": [
        {
            "product_id": "b-uuid",
            "product_type": "book",
            "product_name": "Python Programming",
            "most_common_previous_product_id": "a-uuid",
            "most_common_previous_product_type": "book",
            "most_common_previous_product_name": "Django Basics",
            "occurrence_count": 2
        }
    ],
    "total_carts_analyzed": 10,
    "total_recommendations": 5
}
```

**How It Works:**
The system analyzes the order products are added to carts. If customers frequently add Product B after Product A, it learns that pattern. This enables features like "Customers who bought this also added..." recommendations.

## 🎨 Django Admin Interface

The admin interface makes managing carts a breeze:

### Shopping Cart Admin
- **List View**: Shows all carts with user, creation date, total price, and weight
- **Detail View**: Inline cart items that you can manage directly
- **Read-Only Items**: Existing items are displayed but protected from accidental changes
- **Add New Items**: Easy product selection with filtered content types

### Key Features:
- **Smart Product Selection**: When you select a product type, you see a dropdown of available products (no need to remember UUIDs!)
- **Auto-Population**: Price and weight are automatically filled from the product
- **Cart Summary**: Always visible totals and item counts
- **Filtered Content Types**: Only shows Book, Music Album, and Software License (no clutter)

### Shopping Cart Item Admin
- View all cart items across all carts
- Filter by cart, date, or product type
- See subtotals for each item
- Search by cart ID or product ID

## 💡 The Recommendation Engine

This is one of our favorite features! It's a simple but powerful algorithm:

### How It Works

1. **Data Collection**: Analyzes all shopping carts and notes the order products are added
2. **Pattern Detection**: Tracks sequences like "A → B" (B added after A)
3. **Frequency Counting**: Counts how often each sequence occurs
4. **Recommendation Generation**: For each product, identifies the most common product that precedes it

### Example Scenario

Imagine these shopping patterns:
- Customer 1: Adds Book A, then Book B
- Customer 2: Adds Book A, then Book B again
- Customer 3: Adds Book A, then Book C
- Customer 4: Adds Book C, then Book B

**What We Learn:**
- Book B is most commonly added after Book A (2 times)
- Book C is most commonly added after Book A (1 time)

**Business Value:**
This data can power:
- "Frequently bought together" suggestions
- "Customers also added..." recommendations
- Cross-selling opportunities
- Understanding product relationships

### The Algorithm (In Plain English)

For each shopping cart:
1. Get all items in the order they were added (using timestamps)
2. For each item after the first one, remember what came before it
3. Count how many times each "previous → current" pair appears
4. For each product, pick the most common "previous" product

It's elegant in its simplicity but powerful in its insights!

## 🏗️ Code Organization

### Models (`models.py`)
- **ShoppingCart**: The main cart entity with business logic methods
- **ShoppingCartItem**: Individual items with generic foreign key support
- **Product Models**: Book, MusicAlbum, SoftwareLicense (from this app)

### Views (`views.py`)
- **ShoppingCartViewSet**: All cart-related API endpoints
- Clean, focused actions for each operation
- Proper permission handling

### Serializers (`serializers.py`)
- **ShoppingCartSerializer**: Full cart representation
- **ShoppingCartItemSerializer**: Individual item details
- **ProductRecommendationSerializer**: Recommendation data format
- **AddProductSerializer / RemoveProductSerializer**: Input validation

### Services (`services.py`)
- **calculate_product_recommendations()**: The recommendation algorithm
- Helper functions for product lookup and naming
- Pure business logic (no HTTP concerns)

### Admin (`admin.py`)
- Beautiful inline interfaces
- Smart form handling
- Read-only protections for existing data

## 🔐 Security & Permissions

- **Authentication Required**: All endpoints need a valid JWT token
- **User Isolation**: Users can only access their own carts (unless admin)
- **Admin Access**: Staff users can view all carts with `all_users=true`
- **Data Validation**: All product operations validate product existence
- **Input Sanitization**: UUIDs and product types are validated

## 🧪 Testing the System

### Create a Cart and Add Products
```python
from apps.store.models import ShoppingCart, Book

# Create cart
cart = ShoppingCart.objects.create(user=user)

# Add a book
book = Book.objects.first()
cart.add_product(book, quantity=2)

# Check totals
print(f"Total: €{cart.calculate_total_price()}")
print(f"Weight: {cart.calculate_total_weight()} kg")
```

### Get Recommendations
```python
from apps.store.services import calculate_product_recommendations

# Get all carts
carts = ShoppingCart.objects.all()

# Calculate recommendations
recommendations = calculate_product_recommendations(carts)

# Explore results
for product_key, data in recommendations.items():
    print(f"{data['product_name']} is usually added after {data['most_common_previous_product_name']} ({data['occurrence_count']} times)")
```

## 🎯 Design Decisions

### Why Generic Foreign Keys?

We use Django's ContentType framework instead of separate tables for each product type. This allows:
- One cart item model to handle all product types
- Easy addition of new product types without schema changes
- Unified cart operations regardless of product type

### Why Cached Price/Weight?

When customers add items to their cart, we "lock in" the price they saw. Even if the product price changes later, their cart reflects what they agreed to. This is standard e-commerce practice and ensures fairness.

### Why Service Layer?

Separating business logic into `services.py` means:
- Logic can be reused (admin, API, background tasks)
- Easier to unit test (pure functions)
- Clearer code organization
- Easier to maintain and extend

## 🚀 Real-World Use Cases

### E-Commerce Platform
- Power an online bookstore
- Support multiple product categories
- Enable cross-selling through recommendations

### Library Management
- Track user borrowing patterns
- Suggest related materials
- Understand collection usage

### Analytics & Insights
- Understand product relationships
- Identify cross-selling opportunities
- Analyze shopping patterns

## 📈 Performance Considerations

- **Efficient Queries**: Uses `select_related()` and `prefetch_related()` to minimize database hits
- **Cached Calculations**: Price/weight stored in cart items for fast totals
- **Pagination Ready**: Can handle thousands of carts efficiently
- **Scalable Algorithm**: Recommendation calculation is O(n×m) where n=carts, m=items

## 🔮 Future Enhancements

Ideas for making the system even better:
- **Time-Based Recommendations**: Weight recent patterns more heavily
- **Multi-Item Sequences**: Consider what comes after 2-3 products, not just one
- **Confidence Scores**: Add statistical confidence to recommendations
- **Category Filtering**: Recommendations within product categories
- **Seasonal Patterns**: Learn from time-based shopping trends
- **Cart Abandonment**: Track and analyze abandoned carts
- **Wishlist Integration**: Learn from saved items too

## 💭 Philosophy

We built this system with flexibility in mind. The generic product support means you can add new product types without changing the cart system. The recommendation engine learns from real behavior, not assumptions. And everything is designed to scale from a small store to a large e-commerce platform.

The code is written to be readable—when you look at it in six months, you'll still understand what it does. Comments explain the "why" not just the "what". And the structure makes it easy for new team members to contribute.

---

*Making e-commerce intelligent, flexible, and developer-friendly* 🛒✨

