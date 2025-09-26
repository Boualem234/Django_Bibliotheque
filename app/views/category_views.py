from django.http import Http404
from django.shortcuts import render
from django.views.generic.base import View
from ..models import Category

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