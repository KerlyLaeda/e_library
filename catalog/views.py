from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import DetailView, ListView
from .models import Author, Book, BookInstance, Genre, Language


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
    if request.method == "GET":
        book_search = request.GET.get("q", "").strip()
        if book_search:
            results = Book.objects.filter(title__icontains=book_search)
            if results.exists():
                return render(request, "catalog/search.html", {"results": results, "query": book_search})
            else:  # If no matches are found
                return render(request, "catalog/search.html", {"no_results": True, "query": book_search})
        else:  # Empty query
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def advanced_search(request):
    if request.method == "GET":
        # Fetch all genres and languages for dropdowns
        genres = Genre.objects.all()
        languages = Language.objects.all()

        # Get query parameters
        title_query = request.GET.get("title", "").strip()
        author_query = request.GET.get("author", "").strip()
        genres_query = request.GET.getlist("genres")  # select multiple genres
        language_query = request.GET.getlist("languages")  # select multiple languages
        status_query = request.GET.get("status") == "on"  # checkbox
        publisher_query = request.GET.get("imprint", "").strip()
        isbn_query = request.GET.get("isbn", "").strip()

        # Build the query with Q
        query = Q()
        if title_query:
            query &= Q(title__icontains=title_query)
        if author_query:
            query &= Q(author__last_name__icontains=author_query)
        if genres_query:
            query &= Q(genre__in=genres_query)
        if language_query:
            query &= Q(language__in=language_query)
        if isbn_query:
            query &= Q(isbn=isbn_query)

        # BookInstance-specific filters
        if status_query:
            query &= Q(bookinstance__status="a")
        if publisher_query:
            query &= Q(bookinstance__imprint__icontains=publisher_query)

        # Perform the query
        results = Book.objects.filter(query).distinct().order_by("title")

        context = {
            "results": results,
            "genres": genres,
            "languages": languages,
            "query": {
                "title": title_query,
                "author": author_query,
                "genres": genres_query,
                "languages": language_query,
                "status": status_query,
                "imprint": publisher_query,
                "isbn": isbn_query,
            },
        }

        if results.exists():
            return render(request, "catalog/search.html", context)
        else:
            context["no_results"] = True
            return render(request, "catalog/search.html", context)

    # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # Fallback for GET requests without parameters
    genres = Genre.objects.all()
    languages = Language.objects.all()
    return render(request, "catalog/advanced_search.html", {"genres": genres, "languages": languages})
