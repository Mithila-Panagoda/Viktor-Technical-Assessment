from django.contrib import admin

# Register your models here.
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'publisher', 'publication_date', 'isbn']
    list_filter = ['publication_date']
    search_fields = ['name', 'author', 'publisher', 'isbn']
    ordering = ['id']
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ['publication_date']
    list_display_links = ['name']