from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View

from ..models import Book, Category, Author
from ..forms import BookForm
import datetime

class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        paginator = Paginator(books, 5) 
        page_number = request.GET.get('page') or 1
        context = {
            'range_pages': range(1, paginator.num_pages + 1),
            'page_books': paginator.get_page(page_number),
        }

        return render(request, 'app/book/book_list.html', context)
    
class BookDetailsView(View):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404("Livre non trouvé")
        return render(request, 'app/book/book_details.html', {'book': book})

class AddBookView(PermissionRequiredMixin, View):
    permission_required = "app.add_book"
    template_name = "app/book/book_form.html"

    def get(self, request):
        context = {
            'action_text': 'Ajouter',
            'form': BookForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        
        if form.is_valid():

            form.clean_code()
            title = form.cleaned_data["title"]

            form.save()

            messages.success(
                request,
                f"Livre \"{title}\" ajouté avec succès.",
            )

            return redirect("book_list")
        
        context = {
            'action_text': 'Ajouter',
            'form': form
        }

        return render(request, self.template_name, context)
    
class EditBookView(View):
    permission_required = "app.change_book"
    template_name = "app/book/book_form.html"

    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        context = {
            'action_text': 'Modifier',
            'form': BookForm(instance=book)
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        form = BookForm(request.POST, instance=book)

        if form.is_valid():

            form.clean_code()
            title = form.cleaned_data["title"]

            form.save()

            messages.success(
                request,
                f"Livre \"{title}\" modifié avec succès.",
            )

            return redirect("book_list")

        context = {
            'action_text': 'Modifier',
            'form': form
        }

        return render(request, self.template_name, context)
    
class DelBookView(View):
    permission_required = 'app.delete_book'
    template_name = "app/book/book_confirm_delete.html"

    def get(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        context = {
            'book': book
        }
        return render(request, self.template_name, context)

    def post(self, request, pk):
        book = get_object_or_404(Book, id=pk)
        title = book.title
        book.delete()

        messages.success(
            request,
            f"Livre \"{title}\" supprimé avec succès.",
        )

        return redirect("book_list")