from django.urls import path, re_path
from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.BookListView.as_view(), name="books"),

    # catalog/book/<id> or catalog/books/book/<id> ?
    path("book/<int:pk>", views.BookDetailView.as_view(), name="book-detail"),
    #re_path(r"^book/(?P<slug>[-\w]+)$", views.BookDetailView.as_view(), name="book-detail"),

    path("authors/", views.AuthorListView.as_view(), name="authors"),
    path("author/<int:pk>", views.AuthorDetailView.as_view(), name="author-detail"),

    path("search/", views.search, name="search"),
    path("advanced_search/", views.advanced_search, name="advanced-search")
]
