from django.http import Http404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic.base import View

from ..models import Category
from ..forms import CategoryForm

class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        paginator = Paginator(categories, 5)  
        page_number = request.GET.get('page') or 1
        context = {
            'range_pages': range(1, paginator.num_pages + 1),
            'page_categories': paginator.get_page(page_number),
        }
        return render(request, 'app/category/cat_list.html', context)
    
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
            return redirect("cat_list")

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
            return redirect("cat_list")
        
        context = {
            'action_text': 'Modifier',
            'form': form
        }
        return render(request, self.template_name, context)
    
class DelCategoryView(View):
    permission_required = "app.delete_category"
    template_name = "app/category/category_confirm_delete.html"

    def get(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        return render(request, self.template_name, {'category': category})
    
    def post(self, request, pk):
        category = get_object_or_404(Category, id=pk)
        name = category.name
        category.delete()
        messages.success(request, f"Catégorie \"{name}\" supprimée avec succès.")
        return redirect("cat_list")