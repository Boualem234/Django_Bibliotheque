from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from .models import Book, Category, Author

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class AddBookView(View):
    def get(self, request):
        categories = Category.objects.all()
        authors = Author.objects.all()
        return render(request, 'add_book.html', {'categories': categories, 'authors': authors})
    def post(self, request):
        code = request.POST.get('code')
        title = request.POST.get('title')
        price = request.POST.get('price')
        summary = request.POST.get('summary')
        date = request.POST.get('date')
        edition = request.POST.get('edition')
        category_id = request.POST.get('category')
        author_id = request.POST.get('author')

        category = Category.objects.get(id=category_id)
        author = Author.objects.get(id=author_id)

        book = Book(
            code=code,
            title=title,
            price=price,
            summary=summary,
            date=date,
            edition=edition,
            category=category,
            author=author
        )
        book.save()
        return render(request, 'add_book.html', {'success_message': "Livre ajouté avec succès!"})

    
class BookListView(View):
    def get(self, request):
        books = Book.objects.all()  # Récupère tous les livres
        return render(request, 'book_list.html', {'books': books})
    
class BookDetailsView(View):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Livre non trouvé")
        return render(request, 'book_details.html', {'book': book})