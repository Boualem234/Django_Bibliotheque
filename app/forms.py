from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Book, Author

class CategoryForm(forms.ModelForm):
  template_name = "app/snippets/form_snippet.html"

  class Meta:
    model = Category
    fields = "__all__"
    widgets = {
      'name': forms.TextInput(attrs={'class': 'form-control'}),
    }
  
  def clean_name(self):
    name = self.cleaned_data['name']

    if self.instance.pk is None:
      name_exists = Category.objects.filter(name=name).exists()
    else:
      name_exists = Category.objects.filter(name=name).exclude(id=self.instance.pk).exists()

    if name_exists:
      raise ValidationError("Le nom de catégorie existe déjà")
    
    return name
  
class AuthorForm(forms.ModelForm):
  template_name = "app/snippets/form_snippet.html"

  class Meta:
    model = Author
    fields = "__all__"

    widgets = {
      'first_name': forms.TextInput(attrs={'class': 'form-control'}),
      'last_name': forms.TextInput(attrs={'class': 'form-control'}),
      'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
      'nationality': forms.TextInput(attrs={'class': 'form-control'}),
    }

    def clean(self):
      cleaned_data = super().clean()
      first_name = cleaned_data.get('first_name')
      last_name = cleaned_data.get('last_name')
      birth_date = cleaned_data.get('birth_date')

      if self.instance.pk is None:
        author_exists = Author.objects.filter(first_name=first_name, last_name=last_name, birth_date=birth_date).exists()
      else:
        author_exists = Author.objects.filter(first_name=first_name, last_name=last_name, birth_date=birth_date).exclude(id=self.instance.pk).exists()

      if author_exists:
        raise ValidationError("L'auteur existe déjà")
      
      return cleaned_data

class BookForm(forms.ModelForm):
    template_name = "app/snippets/form_snippet.html"
    
    class Meta:
        model = Book
        fields = ['code', 'title', 'price', 'summary', 'date', 'edition', 'category', 'author', 'image']
    
        widgets = {
        'code': forms.TextInput(attrs={'class': 'form-control'}),
        'title': forms.TextInput(attrs={'class': 'form-control'}),
        'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
        'summary': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'edition': forms.TextInput(attrs={'class': 'form-control'}),
        'category': forms.Select(attrs={'class': 'form-select'}),
        'author': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def clean_code(self):
        code = self.cleaned_data['code']
    
        if self.instance.pk is None:
            code_exists = Book.objects.filter(code=code).exists()
        else:
            code_exists = Book.objects.filter(code=code).exclude(id=self.instance.pk).exists()
    
        if code_exists:
            raise ValidationError("Le code du livre existe déjà")
        
        return code