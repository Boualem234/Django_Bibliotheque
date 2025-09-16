from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('about/', views.AboutView.as_view(), name="about"),
    path('books/', views.BookListView.as_view(), name="book_list"),
    path('categories/', views.CategoryListView.as_view(), name="cat_list"),
    path('authors/', views.AuthorListView.as_view(), name="author_list"),
    path('bookDetails/<int:pk>/', views.BookDetailsView.as_view(), name="book_details"),
    path('catDetails/<int:pk>/', views.CategoryDetailsView.as_view(), name="cat_details"),
    path('authorDetails/<int:pk>/', views.AuthorDetailsView.as_view(), name="author_details"),
    path('addBook/', views.AddBookView.as_view(), name="add_book"),
    path('addCategory/', views.AddCategoryView.as_view(), name="add_category"),
    path('addAuthor/', views.AddAuthorView.as_view(), name="add_author"),
    path('delBook/<int:pk>/', views.DelBookView.as_view(), name="del_book"),
    path('delCategory/<int:pk>/', views.DelCategoryView.as_view(), name="del_cat"),
    path('delAuthor/<int:pk>/', views.DelAuthorView.as_view(), name="del_author"),
    path('editBook/<int:pk>/', views.EditBookView.as_view(), name="edit_book"),
    path('editCategory/<int:pk>/', views.EditCategoryView.as_view(), name="edit_cat"),
    path('editAuthor/<int:pk>/', views.EditAuthorView.as_view(), name="edit_author"),
]