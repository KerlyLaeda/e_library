# Generated by Django 5.1.3 on 2024-12-05 13:04

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0007_remove_book_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='isbn',
            field=models.CharField(max_length=13, unique=True, validators=[django.core.validators.RegexValidator(regex='^\\d{10}(\\d{3})?$')], verbose_name='ISBN'),
        ),
    ]
