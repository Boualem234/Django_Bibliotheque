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
    
class EditBookView(View):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Livre non trouvé")
        categories = Category.objects.all()
        authors = Author.objects.all()
        return render(request, 'edit_book.html', {'book': book, 'categories': categories, 'authors': authors})
    
    def post(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Livre non trouvé")

        book.code = request.POST.get('code')
        book.title = request.POST.get('title')
        book.price = request.POST.get('price')
        book.summary = request.POST.get('summary')
        book.date = request.POST.get('date')
        book.edition = request.POST.get('edition')
        
        category_id = request.POST.get('category')
        author_id = request.POST.get('author')

        book.category = Category.objects.get(id=category_id)
        book.author = Author.objects.get(id=author_id)

        book.save()
        return render(request, 'edit_book.html', {'book': book, 'success_message': "Livre mis à jour avec succès!"})
    
class DelBookView(View):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            books = Book.objects.all()
            return render(request, 'book_list.html', {'books': books, 'success_message': "Livre supprimé avec succès!"})
        except Book.DoesNotExist:
            raise Http404("Livre non trouvé")
        
class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()  # Récupère toutes les catégories
        return render(request, 'cat_list.html', {'categories': categories})
    
class CategoryDetailsView(View):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Catégorie non trouvée")
        return render(request, 'cat_details.html', {'category': category})
    
class AddCategoryView(View):
    def get(self, request):
        return render(request, 'add_category.html')
    
    def post(self, request):
        name = request.POST.get('name')

        category = Category(
            name=name,
        )
        category.save()
        return render(request, 'add_category.html', {'success_message': "Catégorie ajoutée avec succès!"})
    
class DelCategoryView(View):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            categories = Category.objects.all()
            return render(request, 'cat_list.html', {'categories': categories, 'success_message': "Catégorie supprimée avec succès!"})
        except Category.DoesNotExist:
            raise Http404("Catégorie non trouvée")
        
class EditCategoryView(View):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Catégorie non trouvée")
        return render(request, 'edit_category.html', {'category': category})
    
    def post(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Catégorie non trouvée")

        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.save()
        return render(request, 'edit_category.html', {'category': category, 'success_message': "Catégorie mise à jour avec succès!"})
    
class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()  # Récupère tous les auteurs
        return render(request, 'author_list.html', {'authors': authors})
    
class AuthorDetailsView(View):
    def get(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Auteur non trouvé")
        return render(request, 'author_details.html', {'author': author})
    
class AddAuthorView(View):
    def get(self, request):
        return render(request, 'add_author.html')
    
    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        birth_date = request.POST.get('birth_date')
        nationality = request.POST.get('nationality')

        author = Author(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            nationality=nationality)
        
        author.save()
        return render(request, 'add_author.html', {'success_message': "Auteur ajouté avec succès!"})
    
class DelAuthorView(View):
    def get(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
            author.delete()
            authors = Author.objects.all()
            return render(request, 'author_list.html', {'authors': authors, 'success_message': "Auteur supprimé avec succès!"})
        except Author.DoesNotExist:
            raise Http404("Auteur non trouvé")
        
class EditAuthorView(View):
        def get(self, request, pk):
            try:
                author = Author.objects.get(pk=pk)
            except Category.DoesNotExist:
                raise Http404("Catégorie non trouvée")
            return render(request, 'edit_author.html', {'author': author})

        def post(self, request, pk):
            try:
                author = Author.objects.get(pk=pk)
            except Category.DoesNotExist:
                raise Http404("Auteur non trouvée")

            author.first_name = request.POST.get('first_name')
            author.last_name = request.POST.get('last_name')
            author.birth_date = request.POST.get('birth_date')
            author.nationality = request.POST.get('nationality')
            author.save()
            return render(request, 'edit_author.html', {'author': author, 'success_message': "Auteur mis à jour avec succès!"})
    