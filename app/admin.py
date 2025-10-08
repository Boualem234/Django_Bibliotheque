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
    list_display = ['code', 'title', 'price', 'category', 'author', 'date', 'thumbnail']
    search_fields = ['code', 'title', 'author__first_name', 'author__last_name', 'category__name']
    list_filter = ['category', 'author', 'date']
    ordering = ['code', 'title']
    readonly_fields = ['image_preview']
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('code', 'title', 'author', 'category')
        }),
        ('Détails du livre', {
            'fields': ('price', 'date', 'edition', 'summary')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),
            'classes': ('collapse',)
        }),
    )

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="65" style="object-fit: cover; border-radius: 5px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return format_html('<div style="width: 50px; height: 65px; background: #f0f0f0; border-radius: 5px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: #999;">Aucune</div>')
    thumbnail.short_description = "Aperçu"

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '''
                <div style="text-align: center;">
                    <img src="{}" style="max-width: 300px; max-height: 400px; object-fit: contain; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);" />
                    <br><br>
                    <p style="color: #666; font-size: 12px;">
                        <strong>Nom du fichier:</strong> {}<br>
                        <strong>URL:</strong> <a href="{}" target="_blank">{}</a>
                    </p>
                </div>
                ''',
                obj.image.url,
                obj.image.name.split('/')[-1],
                obj.image.url,
                obj.image.url
            )
        return format_html('<p style="color: #999; font-style: italic;">Aucune image sélectionnée</p>')
    image_preview.short_description = "Aperçu de l'image"
