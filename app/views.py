from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from .models import Book, Category, Author

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')
    
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')
    
class AddBookView(View):
    def get(self, request):
        categories = Category.objects.all()
        authors = Author.objects.all()
        return render(request, 'add_book.html', {'categories': categories, 'authors': authors})
    def post(self, request):

        errors = []
        
        code = request.POST.get('code').strip()
        if not code:
            errors.append("Le code est obligatoire.")

        title = request.POST.get('title').strip()
        if not title:
            errors.append("Le titre est obligatoire.")

        price = request.POST.get('price').strip()
        if not price:
            errors.append("Le prix est obligatoire.")

        summary = request.POST.get('summary').strip()

        date = request.POST.get('date').strip()
        if not date:
            errors.append("La date de publication est obligatoire.")

        edition = request.POST.get('edition').strip()
        if not edition:
            errors.append("L'édition est obligatoire.")

        category_id = request.POST.get('category')
        if not category_id:
            errors.append("La catégorie est obligatoire.")

        author_id = request.POST.get('author')
        if not author_id:   
            errors.append("L'auteur est obligatoire.")


        if errors:
            categories = Category.objects.all()
            authors = Author.objects.all()
            return render(request, 'add_book.html', {'categories': categories, 'authors': authors, 'errors': errors})

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

        try:
            book.save()
        except Exception as e:
            categories = Category.objects.all()
            authors = Author.objects.all()
            return render(request, 'add_book.html', {'categories': categories, 'authors': authors, 'error_message': str(e)})
        
        return render(request, 'add_book.html', {'success_message': "Livre ajouté avec succès!"})

    
class BookListView(View):
    def get(self, request):
        books = Book.objects.all() 
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
            
        errors = []
        
        code = request.POST.get('code').strip()
        if not code:
            errors.append("Le code est obligatoire.")

        title = request.POST.get('title').strip()
        if not title:
            errors.append("Le titre est obligatoire.")

        price = request.POST.get('price').strip()
        if not price:
            errors.append("Le prix est obligatoire.")

        summary = request.POST.get('summary').strip()

        date = request.POST.get('date').strip()
        if not date:
            errors.append("La date de publication est obligatoire.")

        edition = request.POST.get('edition').strip()
        if not edition:
            errors.append("L'édition est obligatoire.")

        category_id = request.POST.get('category')
        if not category_id:
            errors.append("La catégorie est obligatoire.")

        author_id = request.POST.get('author')
        if not author_id:   
            errors.append("L'auteur est obligatoire.")

        if errors:
            categories = Category.objects.all()
            authors = Author.objects.all()
            return render(request, 'edit_book.html', {'book': book, 'categories': categories, 'authors': authors, 'errors': errors})

        book.category = Category.objects.get(id=category_id)
        book.author = Author.objects.get(id=author_id)

        try:
            book.save()
        except Exception as e:
            categories = Category.objects.all()
            authors = Author.objects.all()
            return render(request, 'edit_book.html', {'book': book, 'categories': categories, 'authors': authors, 'error_message': str(e)})
        
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
        categories = Category.objects.all() 
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
        name = request.POST.get('name').strip()

        errors = []
        if not name:
            errors.append("Le nom est obligatoire.")
        if errors:
            return render(request, 'add_category.html', {'errors': errors})

        category = Category(
            name=name,
        )

        try:
            category.save()
        except Exception as e:
            return render(request, 'add_category.html', {'error_message': str(e)})
        
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

        name = request.POST.get('name').strip()
        if not name:
            return render(request, 'edit_category.html', {'category': category, 'error_message': "Le nom est obligatoire."})

        category.name = name

        try:
            category.save()
        except Exception as e:
            return render(request, 'edit_category.html', {'category': category, 'error_message': str(e)})
    
        return render(request, 'edit_category.html', {'category': category, 'success_message': "Catégorie mise à jour avec succès!"})
    
class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all() 
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

        errors = []

        first_name = request.POST.get('first_name').strip()
        if not first_name:
            errors.append("Le prénom est obligatoire.")
        last_name = request.POST.get('last_name').strip()
        if not last_name:
            errors.append("Le nom est obligatoire.")
        birth_date = request.POST.get('birth_date').strip()
        if not birth_date:
            errors.append("La date de naissance est obligatoire.")
        nationality = request.POST.get('nationality').strip()
        if not nationality:
            errors.append("La nationalité est obligatoire.")

        if errors:
            return render(request, 'add_author.html', {'errors': errors})

        author = Author(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            nationality=nationality)
        
        try:
            author.save()
        except Exception as e:
            return render(request, 'add_author.html', {'error_message': str(e)})
        
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

            errors = []

            first_name = request.POST.get('first_name').strip()
            if not first_name:
                errors.append("Le prénom est obligatoire.")
            last_name = request.POST.get('last_name').strip()
            if not last_name:
                errors.append("Le nom est obligatoire.")
            birth_date = request.POST.get('birth_date').strip()
            if not birth_date:
                errors.append("La date de naissance est obligatoire.")
            nationality = request.POST.get('nationality').strip()
            if not nationality:
                errors.append("La nationalité est obligatoire.")
            if errors:
                return render(request, 'edit_author.html', {'author': author, 'errors': errors})

            try:
                author.save()
            except Exception as e:
                return render(request, 'edit_author.html', {'author': author, 'error_message': str(e)})
            
            return render(request, 'edit_author.html', {'author': author, 'success_message': "Auteur mis à jour avec succès!"})
    