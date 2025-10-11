from modeltranslation.translator import translator, TranslationOptions
from .models import Author, Category, Book

class BookTranslationOptions(TranslationOptions):
    fields = ('title', 'summary', 'edition')

translator.register(Book, BookTranslationOptions)

class AuthorTranslationOptions(TranslationOptions):
    fields = ('nationality',)

translator.register(Author, AuthorTranslationOptions)

class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

translator.register(Category, CategoryTranslationOptions)
