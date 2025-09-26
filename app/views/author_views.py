from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from ..models import Book, Category, Author
import datetime

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
        else:
            try:
                pub_date = datetime.date.fromisoformat(birth_date)
                if pub_date > datetime.date.today():
                    errors.append("La date de naissance ne peut pas être dans le futur.")
            except ValueError:
                errors.append("La date de naissance n’est pas valide.")

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
            else:
                try:
                    pub_date = datetime.date.fromisoformat(birth_date)
                    if pub_date > datetime.date.today():
                        errors.append("La date de naissance ne peut pas être dans le futur.")
                except ValueError:
                    errors.append("La date de naissance n’est pas valide.")
                    
            nationality = request.POST.get('nationality').strip()
            if not nationality:
                errors.append("La nationalité est obligatoire.")
            if errors:
                return render(request, 'edit_author.html', {'author': author, 'errors': errors})

            author.first_name = first_name
            author.last_name = last_name
            author.birth_date = birth_date
            author.nationality = nationality

            try:
                author.save()
            except Exception as e:
                return render(request, 'edit_author.html', {'author': author, 'error_message': str(e)})
            
            return render(request, 'edit_author.html', {'author': author, 'success_message': "Auteur mis à jour avec succès!"})