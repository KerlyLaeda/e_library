from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView
from django.utils.timezone import now
from .models import Author, Book, BookInstance, Genre, Language
import datetime


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
        # If user submits an empty form,
        # render the current page without displaying all books in db
        # Check if the query is empty
        is_empty_query = all(
            not request.GET.get(param, "").strip()
            for param in ["title", "author", "genres", "languages", "imprint", "isbn"]
        ) and not request.GET.get("status")

        if is_empty_query:
            # Redirect to the current page without resetting parameters
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        # Fetch all genres and languages for select fields
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

    # Fallback for GET requests without parameters
    genres = Genre.objects.all()
    languages = Language.objects.all()
    return render(request, "catalog/search.html", {"genres": genres, "languages": languages})


# make it class method
@login_required
def borrow(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":

        # Check if the user already borrowed a copy of this book
        if BookInstance.objects.filter(book=book, borrower=request.user, status="o").exists():
            messages.error(request, "You have already borrowed this book.")
            return redirect("book-detail", pk=book.pk)

        # Borrow the book
        instance = book.bookinstance_set.filter(status="a").first()
        if instance:
            instance.status = "o"
            instance.borrower = request.user
            instance.due_back = now() + datetime.timedelta(weeks=2)
            instance.save()
            messages.success(request, f'You borrowed "{book.title}"!')
            return redirect("book-detail", pk=book.pk)
    else:
        # No available copies
        messages.error(request, f'Sorry, "{book.title}" is not available. You can reserve it clicking the button below')  # change this
        return redirect("book-detail", pk=book.pk)
    return redirect("index")


class LoanedByUserView(LoginRequiredMixin, ListView):
    """Generic view listing books on loan to current user."""
    model = BookInstance
    template_name = "catalog/bookinstance_list_borrowed_user.html"
    paginate_by = 10  # remove if add quantity restriction

    def get_queryset(self):
        return (BookInstance.objects.filter(borrower=self.request.user)
                .filter(status__exact="o")
                .order_by("due_back"))


# user can return clicking a button, also need autoreturn if expired
@login_required
def return_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        instance = book.bookinstance_set.filter(status="o", borrower=request.user).first()  # ?
        if instance:
            instance.status = "a"
            instance.borrower = None
            instance.due_back = None
            instance.save()
            return redirect("user-borrowed")
    return redirect("index")
