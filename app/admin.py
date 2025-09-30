from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Book, Author


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'book_count']
    ordering = ['name']
    search_fields = ['name']
    
    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Nombre de livres"
    

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'birth_date', 'nationality', 'book_count']
    search_fields = ['first_name', 'last_name', 'nationality']
    list_filter = ['nationality']
    ordering = ['last_name', 'first_name']

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    full_name.short_description = "Nom complet"

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = "Nombre de livres"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['code', 'title', 'price', 'category', 'author', 'date', 'image_tag']
    search_fields = ['code', 'title', 'author__first_name', 'author__last_name', 'category__name']
    list_filter = ['category', 'author', 'date']
    ordering = ['code', 'title']
    readonly_fields = ['image_tag']
    exclude = []

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="60" height="80" style="object-fit: cover;" />', obj.image.url)
        return "-"
    image_tag.short_description = "Image du livre"
