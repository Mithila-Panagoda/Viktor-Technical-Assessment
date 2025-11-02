"""
Service layer for store app business logic.
"""
from collections import defaultdict, Counter
from .models import Book, MusicAlbum, SoftwareLicense


def calculate_product_recommendations(carts):
    """
    Calculate product recommendations based on the order products are added to carts.
    
    For each product, finds the most common product that was added before it.
    
    Args:
        carts: QuerySet or list of ShoppingCart instances
        
    Returns:
        dict: Dictionary mapping product identifiers to recommendation data
        {
            'product_key': {
                'product_id': str,
                'product_type': str,
                'product_name': str,
                'most_common_previous_product_id': str or None,
                'most_common_previous_product_type': str or None,
                'most_common_previous_product_name': str or None,
                'occurrence_count': int
            }
        }
    """
    # Dictionary to track (previous_product, current_product) pairs and their counts
    product_sequences = defaultdict(Counter)
    
    # Process each cart
    for cart in carts:
        # Get all items ordered by created_at (order they were added)
        items = cart.items.select_related('content_type').order_by('created_at').all()
        
        if not items:
            continue
        
        # Convert items to list for easier iteration
        items_list = list(items)
        
        # Track sequences: for each item (except first), record what came before it
        for i in range(1, len(items_list)):
            current_item = items_list[i]
            previous_item = items_list[i - 1]
            
            # Create unique keys for products
            previous_key = f"{previous_item.content_type.model}:{previous_item.object_id}"
            current_key = f"{current_item.content_type.model}:{current_item.object_id}"
            
            # Increment count for this sequence
            product_sequences[current_key][previous_key] += 1
    
    # Build recommendation results
    recommendations = {}
    
    for current_key, previous_counts in product_sequences.items():
        if not previous_counts:
            continue
        
        # Find the most common previous product
        most_common_previous_key, occurrence_count = previous_counts.most_common(1)[0]
        
        # Parse current product info
        current_type, current_id = current_key.split(':')
        
        # Parse previous product info
        prev_type, prev_id = most_common_previous_key.split(':')
        
        # Get product instances for names
        current_product = None
        previous_product = None
        try:
            current_product = _get_product_by_type_and_id(current_type, current_id)
            previous_product = _get_product_by_type_and_id(prev_type, prev_id)
            
            current_name = _get_product_name(current_product)
            previous_name = _get_product_name(previous_product) if previous_product else None
        except Exception:
            current_name = f"{current_type} {current_id}"
            previous_name = f"{prev_type} {prev_id}" if previous_product else None
        
        recommendations[current_key] = {
            'product_id': current_id,
            'product_type': current_type,
            'product_name': current_name,
            'most_common_previous_product_id': prev_id,
            'most_common_previous_product_type': prev_type,
            'most_common_previous_product_name': previous_name,
            'occurrence_count': occurrence_count
        }
    
    return recommendations


def _get_product_by_type_and_id(product_type, product_id):
    """
    Helper function to get product instance by type and id.
    
    Args:
        product_type: ContentType model name (e.g., 'book', 'musicalbum', 'softwarelicense')
        product_id: UUID string of the product
        
    Returns:
        Product instance (Book, MusicAlbum, or SoftwareLicense) or None
    """
    from django.contrib.contenttypes.models import ContentType
    
    try:
        content_type = ContentType.objects.get(model=product_type.lower())
        model_class = content_type.model_class()
        if model_class:
            return model_class.objects.get(id=product_id)
    except Exception:
        return None
    return None


def _get_product_name(product):
    """
    Helper function to get product name for display.
    
    Args:
        product: Product instance (Book, MusicAlbum, or SoftwareLicense)
        
    Returns:
        str: Human-readable product name or None
    """
    if not product:
        return None
    
    if isinstance(product, Book):
        return product.title
    elif isinstance(product, MusicAlbum):
        return f"Album by {product.artist}"
    elif isinstance(product, SoftwareLicense):
        return f"License {product.id}"
    return str(product)

