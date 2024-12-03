from django.contrib import admin
from .models import (
    Author,
    Book,
    BookInstance,
    Genre,
    Language
)


class BooksInline(admin.TabularInline):
    """
    Inline admin class for displaying books associated with an author.

    Attributes:
        model (Model): The model class for the inline form.
        extra (int): The number of extra forms the formset will display in addition to the initial forms.
    """
    model = Book
    extra = 0  # to remove placeholders for instances


class BooksInstanceInline(admin.TabularInline):
    """
    Inline admin class for displaying book instances associated with a book.

    Attributes:
        model (Model): The model class for the inline form.
        extra (int): The number of extra forms the formset will display in addition to the initial forms.
    """
    model = BookInstance
    extra = 0


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.

    Attributes:
        list_display (tuple): Fields to display in the change list page.
        inlines (list): Inline forms to display related models.

    This class configures the admin interface for managing Author objects,
    allowing users to view author details and manage associated books.
    """
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    inlines = [BooksInline]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.

    Attributes:
        list_display (tuple): Fields to display in the change list page.
        inlines (list): Inline forms to display related models.

    This class configures the admin interface for managing Book objects,
    allowing users to view book details and manage associated book instances.
    """
    list_display = ("title", "author", "display_genre")
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    """
    Admin configuration for the BookInstance model.

    Attributes:
        list_display (tuple): Fields to display in the change list page.
        list_filter (list): Filters available in the change list page.
        fieldsets (tuple): Groups of fields displayed in the form page.

    This class configures the admin interface for managing BookInstance objects,
    allowing users to view book instance details, filter by status and due date,
    and manage availability information.
    """
    list_display = ("book", "status", "due_back", "id")
    list_filter = ("status", "due_back")

    fieldsets = (
        (None, {
            "fields": ("book", "imprint", "id")
        }),
        ("Availability", {
            "fields": ("status", "due_back")
        }),
    )


try:
    admin.site.register(Author, AuthorAdmin)
    admin.site.register(Book, BookAdmin)
    admin.site.register(BookInstance, BookInstanceAdmin)
except admin.sites.AlreadyRegistered:
    admin.site.unregister(Author)
    admin.site.unregister(Book)
    admin.site.unregister(BookInstance)

    admin.site.register(Author, AuthorAdmin)
    admin.site.register(Book, BookAdmin)
    admin.site.register(BookInstance, BookInstanceAdmin)

# admin.site.register(Author)
# admin.site.register(Book)
# admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)

# When you define a custom user admin in your app's admin.py, you must first unregister the default User model admin before registering your own.
#
# admin.site.unregister(User)
# admin.site.register(User, MyUserAdmin)