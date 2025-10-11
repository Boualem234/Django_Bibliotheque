from django.shortcuts import render, redirect
from django.views.generic.base import View
from app.models import Book, Author, Category
from django.utils import translation
from django.http import HttpResponseRedirect

class IndexView(View):
    def get(self, request):
        search_query = request.GET.get('search', '').strip()
        
        if search_query:
            # Redirection vers la page de liste avec la recherche
            return redirect(f"/books/?search={search_query}")
        
        featured_books = Book.objects.filter(image__isnull=False).exclude(image='')[:3]
        context = {
            'featured_books': featured_books,
            'books_count': Book.objects.count(),
            'authors_count': Author.objects.count(),
            'categories_count': Category.objects.count(),
        }
        return render(request, 'index.html', context)
    
class AboutView(View):
    def get(self, request):
        current_lang = translation.get_language()
        print("LANGUAGE ACTIVE:", current_lang)
        return render(request, 'about.html')
