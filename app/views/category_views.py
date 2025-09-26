from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View

from ..models import Category
from ..forms import CategoryForm

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all() 
        return render(request, 'app/category/cat_list.html', {'categories': categories})
    
class CategoryDetailsView(View):
    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            raise Http404("Catégorie non trouvée")
        return render(request, 'app/category/cat_details.html', {'category': category})
    
class AddCategoryView(PermissionRequiredMixin, View):
    permission_required = 'app.add_category'
    template_name = "app/category/category_form.html"

    def get(self, request):
        context = {
            'action_text': 'Ajouter',
            'form': CategoryForm()
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            name = form.cleaned_data["name"]
            form.save()
            messages.success(
                request,
                f"Catérorie \"{name}\" ajoutée avec succès.",
            )
            return redirect("category_list")

        context = {
            'action_text': 'Ajouter',
            'form': form
        }
        return render(request, self.template_name, context)

    
class EditCategoryView(View):
    permission_required = "app.change_category"
    template_name = "app/category/category_form.html"

    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        context = {
            'action_text': 'Modifier',
            'form': CategoryForm(instance=category)
        }
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        form = CategoryForm(request.POST, instance=category)
        
        if form.is_valid():
            form.save()
            messages.success(
                request,
                f"Catérorie \"{category.name}\" modifiée avec succès.",
            )
            return redirect("category", category.id)
        
        context = {
            'action_text': 'Modifier',
            'form': form
        }
        return render(request, self.template_name, context)
    
class DelCategoryView(View):
    permission_required = "app.delete_category"

    def get(self, request, pk):
        try:
            category = get_object_or_404(Category, id=pk)
            category.delete()
            messages.success(
                request,
                f"Catérorie \"{category.name}\" supprimée avec succès.",
            )
        except Category.DoesNotExist:
            pass
        return redirect("category_list")