import uuid

from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.RESTRICT, null=True)  # handle > 1 authors?
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book.")
    isbn = models.CharField("ISBN", max_length=13, unique=True)
    genre = models.ManyToManyField("Genre")
    language = models.ForeignKey("Language", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField(blank=True, null=True)
    dod = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])

    class Meta:
        ordering = ["last_name", "first_name"]


class Genre(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="Enter a book genre")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a particular genre instance."""
        return reverse("genre-detail", args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="genre_name_case_insensitive_unique",
                violation_error_message="Genre already exists"
            ),
        ]


class BookInstance(models.Model):
    """Model representing a specific copy of a book that can be borrowed."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this book across whole library")
    due_back = models.DateField(null=True, blank=True)
    book = models.ForeignKey(Book, on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    #borrower = User

    LOAN_STATUS = (
        ("a", "Available"),
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("r", "Reserved"),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default="m")

    def __str__(self):
        return f"{self.id} ({self.book.title})"

    class Meta:
        ordering = ["due_back"]


class Language(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("language-detail", args=[str(self.id)])

    class Meta:
        constraints = [
            UniqueConstraint(
                Lower("name"),
                name="language_name_case_insensitive_unique",
                violation_error_message="Language already exists"
            )
        ]
