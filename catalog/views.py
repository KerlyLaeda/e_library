from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Author, Book, BookInstance


# change index's content later
# what should be on homepage?
def index(request):
    books_num = Book.objects.all().count()
    copies_num = BookInstance.objects.all().count()
    copies_available = BookInstance.objects.filter(status__exact="a").count()
    authors_num = Author.objects.all().count()

    context = {
        "books_num": books_num,
        "instances_num": copies_num,
        "copies_available": copies_available,
        "authors_num": authors_num
    }

    return render(request, "catalog/index.html", context)


class BookListView(ListView):
    model = Book
    paginate_by = 10


class BookDetailView(DetailView):
    model = Book


class AuthorListView(ListView):
    model = Author
    paginate_by = 10


class AuthorDetailView(DetailView):
    model = Author
