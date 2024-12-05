# Generated by Django 5.1.3 on 2024-12-04 15:53

from django.db import migrations, models
from django.utils.text import slugify
import uuid


# def generate_unique_slugs(apps, schema_editor):
#     Book = apps.get_model("catalog", "Book")
#     for book in Book.objects.all():
#         if not book.slug:
#             unique_slug = slugify(book.title)
#             while Book.objects.filter(slug=unique_slug).exists():
#                 unique_slug = f"{slugify(book.title)}-{uuid.uuid4().hex[:8]}"
#             book.slug = unique_slug
#             book.save()


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_rename_dob_author_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        # migrations.RunPython(generate_unique_slugs),
    ]