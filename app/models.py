from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_not_future(value):
    if value > timezone.now().date():
        raise ValidationError("La date ne peut pas être dans le futur.")

class Category(models.Model):
  name = models.CharField(max_length=50,unique=True, verbose_name="Nom")

  def __str__(self):
    return self.name

  class Meta:
    ordering = ('name', )
    verbose_name = "catégorie"
    verbose_name_plural = "catégories"

class Author(models.Model):
  first_name = models.CharField(max_length=50,verbose_name="Prénom")
  last_name= models.CharField(max_length=50,verbose_name="Nom de famille")
  birth_date= models.DateField(verbose_name="Date de naissance",validators=[validate_not_future])
  nationality= models.CharField(max_length=50,verbose_name="Nationnalité")
  
  def __str__(self):
     return '{} - {}'.format(self.last_name, self.first_name)

  class Meta:
    ordering = ('last_name', )
    verbose_name = "auteur"
    verbose_name_plural = "auteurs"

class Book(models.Model):
  code = models.CharField(max_length=15, unique=True, verbose_name="Code du livre")
  title = models.CharField(max_length=50, verbose_name="Titre du livre")
  price = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(1)], verbose_name="Prix du livre")
  summary = models.CharField(max_length=200, verbose_name="Résumé du livre",blank=True)
  date = models.DateField(verbose_name = "Date de publication",validators=[validate_not_future])
  edition = models.CharField(verbose_name = "Edition du livre")
  category = models.ForeignKey(Category, verbose_name="Catégorie", related_name='books', on_delete=models.CASCADE)
  author = models.ForeignKey(Author, verbose_name="Auteurs", related_name='books', on_delete=models.CASCADE)
  image = models.ImageField(default="", upload_to='books/', verbose_name="Image")

  def __str__(self):
    return '{} - {}'.format(self.code, self.title)

  class Meta:
    ordering = ('code', 'title', )
    verbose_name = "book"
    verbose_name_plural = "books"


