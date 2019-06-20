from django.db import models
from django.utils import timezone

class BookCategory(models.Model):
    book_category = models.CharField(max_length=200)
    book_category_slug = models.CharField(max_length=200, default=1)
    class Meta():
        verbose_name_plural = "Categories"
    def __str__(self):
        return self.book_category
