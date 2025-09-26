from django.urls import path

from .views import *

urlpatterns = [
    path('', IndexView.as_view(), name="index"),

    path('about/', AboutView.as_view(), name="about"),
    path('books/', BookListView.as_view(), name="book_list"),
    path('categories/', CategoryListView.as_view(), name="cat_list"),
    path('authors/', AuthorListView.as_view(), name="author_list"),
    path('bookDetails/<int:pk>/', BookDetailsView.as_view(), name="book_details"),
    path('catDetails/<int:pk>/', CategoryDetailsView.as_view(), name="cat_details"),
    path('authorDetails/<int:pk>/', AuthorDetailsView.as_view(), name="author_details"),
    path('addBook/', AddBookView.as_view(), name="add_book"),
    path('addCategory/', AddCategoryView.as_view(), name="add_category"),
    path('addAuthor/', AddAuthorView.as_view(), name="add_author"),
    path('delBook/<int:pk>/', DelBookView.as_view(), name="del_book"),
    path('delCategory/<int:pk>/', DelCategoryView.as_view(), name="del_cat"),
    path('delAuthor/<int:pk>/', DelAuthorView.as_view(), name="del_author"),
    path('editBook/<int:pk>/', EditBookView.as_view(), name="edit_book"),
    path('editCategory/<int:pk>/', EditCategoryView.as_view(), name="edit_cat"),
    path('editAuthor/<int:pk>/', EditAuthorView.as_view(), name="edit_author"),
]