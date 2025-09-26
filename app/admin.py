from django.contrib import admin
from .models import Category, Book, Author

admin.site.register(Book)
#admin.site.register(Product)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name',]
    ordering = ['name',]
    #readonly_fields = ['code']
    search_fields = ['code', 'name']

admin.site.register(Author)



######          FAIRE ADMIN         ######