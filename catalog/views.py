from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Author, Book, BookInstance


# change index's content later
# what should be on homepage?
def index(request):
    books_num = Book.objects.count()
    copies_num = BookInstance.objects.count()
    copies_available = BookInstance.objects.filter(status__exact="a").count()
    authors_num = Author.objects.count()

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


def search(request):
    if request.method == "POST":
        book_search = request.POST.get("q", "").strip()
        if book_search:
            results = Book.objects.filter(title__icontains=book_search)
            if results.exists():
                return render(request, "catalog/search.html", {"results": results, "query": book_search})
            else:  # If no matches are found
                return render(request, "catalog/search.html", {"no_results": True, "query": book_search})
        else:  # Empty query
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

