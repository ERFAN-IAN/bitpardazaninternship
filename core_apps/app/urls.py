from django.contrib import admin
from django.urls import path, include
from .views import (
    AuthorListView,
    AuthorCreateView,
    AuthorUpdateView,
    AuthorDeleteView,
    AuthorDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
)

urlpatterns = [
    path("", AuthorListView.as_view(), name="home"),
    path("add_author", AuthorCreateView.as_view(), name="add_author"),
    path("edit_author/<int:pk>", AuthorUpdateView.as_view(), name="edit_author"),
    path("delete_author/<int:pk>", AuthorDeleteView.as_view(), name="delete_author"),
    path("author_detail/<int:pk>", AuthorDetailView.as_view(), name="author_detail"),
    path("add_book/<int:pk>", BookCreateView.as_view(), name="add_book"),
    path("edit_book/<int:pk>", BookUpdateView.as_view(), name="edit_book"),
    path("delete_book/<int:pk>", BookDeleteView.as_view(), name="delete_book"),
]
