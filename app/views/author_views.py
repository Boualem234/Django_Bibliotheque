from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View
from django.utils.translation import gettext_lazy as _

from ..models import Author
from ..forms import AuthorForm

class AuthorListView(View):
    def get(self, request):
        authors = Author.objects.all()
        paginator = Paginator(authors, 5)
        page_number = request.GET.get('page') or 1
        context = {
            'range_pages': range(1, paginator.num_pages + 1),
            'page_authors': paginator.get_page(page_number),
        }
        return render(request, 'app/author/author_list.html', context)

class AuthorDetailsView(View):
    def get(self, request, pk):
        try:
            author = Author.objects.get(pk=pk)
        except Author.DoesNotExist:
            raise Http404("Auteur non trouvé")
        return render(request, 'app/author/author_details.html', {'author': author})

class AddAuthorView(PermissionRequiredMixin, View):
    permission_required = 'app.add_author'
    template_name = "app/author/author_form.html"

    def get(self, request):
        context = {
            'action_text': _('Ajouter'),
            'form': AuthorForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = AuthorForm(request.POST)
        
        if form.is_valid():
            author = form.save()
            messages.success(
                request,
                f"Auteur \"{author.first_name} {author.last_name}\" ajouté avec succès.",
            )
            return redirect("author_list")

        context = {
            'action_text': _('Ajouter'),
            'form': form
        }
        return render(request, self.template_name, context)

class EditAuthorView(PermissionRequiredMixin, View):
    permission_required = "app.change_author"
    template_name = "app/author/author_form.html"

    def get(self, request, pk):
        author = get_object_or_404(Author, id=pk)
        context = {
            'action_text': _('Modifier'),
            'form': AuthorForm(instance=author)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        author = get_object_or_404(Author, id=pk)
        form = AuthorForm(request.POST, instance=author)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Auteur \"{author.first_name} {author.last_name}\" modifié avec succès.",
            )
            return redirect("author_list")
        
        context = {
            'action_text': _('Modifier'),
            'form': form
        }
        return render(request, self.template_name, context)

class DelAuthorView(PermissionRequiredMixin, View):
    permission_required = "app.delete_author"
    template_name = "app/author/author_confirm_delete.html"

    def get(self, request, pk):
        author = get_object_or_404(Author, id=pk)
        return render(request, self.template_name, {'author': author})
    
    def post(self, request, pk):
        author = get_object_or_404(Author, id=pk)
        name = f"{author.first_name} {author.last_name}"
        author.delete()
        messages.success(request, f"Auteur \"{name}\" supprimé avec succès.")
        return redirect("author_list")