from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Book, BookInstance


NUM_COPIES = 5


@receiver(post_save, sender=Book)
def create_book_copies(sender, instance, created, **kwargs):
    if created:
        if not BookInstance.objects.filter(book=instance).exists():
            for _ in range(NUM_COPIES):
                BookInstance.objects.create(book=instance, imprint="Default Imprint", status="a")  # handle imprints later
