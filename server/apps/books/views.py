from django.shortcuts import render

# Create your views here.
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    tags = ['Book']
    
    # Filtering and ordering
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    
    # Filter fields - allows filtering on all model fields
    filterset_fields = [
        'name',
        'author',
        'publisher',
        'publication_date',
        'isbn',
        # 'cover_photo',
    ]
    
    # Search fields - allows search across multiple fields
    search_fields = [
        'name',
        'author',
        'publisher',
        'isbn',
    ]
    
    # Ordering fields - allows sorting on all fields (ascending/descending)
    ordering_fields = [
        'id',
        'name',
        'author',
        'publisher',
        'publication_date',
        'isbn',
    ]
    
    # Default ordering
    ordering = ['id']