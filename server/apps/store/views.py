from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import ShoppingCart
from .serializers import (
    ShoppingCartSerializer,
    AddProductSerializer,
    RemoveProductSerializer,
    ProductRecommendationSerializer
)
from .services import calculate_product_recommendations


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing shopping carts.
    
    Provides endpoints to:
    - List and retrieve shopping carts
    - Create a new shopping cart
    - Add products to cart
    - Remove products from cart
    - Get cart totals
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]
    tags = ['Shopping Cart']
    
    def get_queryset(self):
        """Return shopping carts for the authenticated user."""
        return ShoppingCart.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        """Automatically assign the cart to the authenticated user."""
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'], url_path='add-product')
    def add_product(self, request, pk=None):
        """
        Add a product to the shopping cart.
        
        Expected payload:
        {
            "product_type": "book" | "musicalbum" | "softwarelicense",
            "product_id": "uuid",
            "quantity": 1 (optional, defaults to 1)
        }
        """
        cart = self.get_object()
        serializer = AddProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data.get('quantity', 1)
            
            cart_item = cart.add_product(product, quantity)
            
            # Return updated cart
            cart_serializer = ShoppingCartSerializer(cart)
            return Response(
                {
                    'message': f'Product added to cart successfully',
                    'cart': cart_serializer.data
                },
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'], url_path='remove-product')
    def remove_product(self, request, pk=None):
        """
        Remove a product from the shopping cart.
        
        Expected payload:
        {
            "product_type": "book" | "musicalbum" | "softwarelicense",
            "product_id": "uuid",
            "quantity": 1 (optional, defaults to 1)
        }
        """
        cart = self.get_object()
        serializer = RemoveProductSerializer(data=request.data)
        
        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data.get('quantity', 1)
            
            removed = cart.remove_product(product, quantity)
            
            if removed:
                # Return updated cart
                cart_serializer = ShoppingCartSerializer(cart)
                return Response(
                    {
                        'message': 'Product removed from cart successfully',
                        'cart': cart_serializer.data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'message': 'Product not found in cart'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='totals')
    def get_totals(self, request, pk=None):
        """
        Get the total price and weight of all items in the cart.
        """
        cart = self.get_object()
        
        return Response({
            'cart_id': str(cart.id),
            'total_price': str(cart.calculate_total_price()),
            'total_weight': str(cart.calculate_total_weight()),
            'item_count': cart.items.count(),
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='my-cart')
    def get_my_cart(self, request):
        """
        Get or create the current user's active shopping cart.
        """
        cart, created = ShoppingCart.objects.get_or_create(
            user=request.user
        )
        
        serializer = self.get_serializer(cart)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED
        )
    
    @action(detail=True, methods=['delete'], url_path='clear')
    def clear_cart(self, request, pk=None):
        """
        Remove all items from the shopping cart.
        """
        cart = self.get_object()
        cart.items.all().delete()
        
        serializer = self.get_serializer(cart)
        return Response(
            {
                'message': 'Cart cleared successfully',
                'cart': serializer.data
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['get'], url_path='recommendations')
    def get_recommendations(self, request):
        """
        Get product recommendations based on the order products are added to carts.
        
        Analyzes all shopping carts and calculates for each product:
        - The most common product that was added before it
        - The number of occurrences
        
        Query Parameters:
        - user_id (optional): Filter recommendations based on a specific user's carts
        - all_users (optional): If true, analyze all carts (admin only)
        """
        # Get carts to analyze
        user_id = request.query_params.get('user_id')
        all_users = request.query_params.get('all_users', 'false').lower() == 'true'
        
        if all_users and request.user.is_staff:
            # Admin can view all carts
            carts = ShoppingCart.objects.prefetch_related('items__content_type').all()
        elif user_id and (request.user.is_staff or str(request.user.id) == user_id):
            # User can view their own carts or admin can view any user's carts
            carts = ShoppingCart.objects.prefetch_related('items__content_type').filter(user_id=user_id)
        else:
            # Default: user's own carts
            carts = ShoppingCart.objects.prefetch_related('items__content_type').filter(user=request.user)
        
        # Calculate recommendations
        recommendations_dict = calculate_product_recommendations(carts)
        
        # Convert to list for serialization
        recommendations_list = list(recommendations_dict.values())
        
        # Serialize and return
        serializer = ProductRecommendationSerializer(recommendations_list, many=True)
        
        return Response({
            'recommendations': serializer.data,
            'total_carts_analyzed': carts.count(),
            'total_recommendations': len(recommendations_list)
        }, status=status.HTTP_200_OK)
