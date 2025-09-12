from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('books/', views.BookListView.as_view(), name="book_list"),
    path('bookDetails/<int:pk>/', views.BookDetailsView.as_view(), name="book_details"),
    path('addBook/', views.AddBookView.as_view(), name="add_book"),
]