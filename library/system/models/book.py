from django.db import models
from django.utils import timezone

from .choices import SECTION_CHOICES, ROW_CHOICES, RACK_CHOICES, RACK_LEVEL_CHOICES
from .user import User
from .bookcategory import BookCategory

class Book(models.Model):
    book_title = models.CharField(max_length=200)
    book_author = models.CharField(max_length=200)
    book_published_date = models.DateTimeField('date published', default=None, null=True, blank=True)
    book_category = models.ForeignKey(BookCategory, default=None, verbose_name="Category", on_delete=models.SET_DEFAULT)
    book_summary = models.TextField(default=None, null=True, blank=True)
    book_slug = models.CharField(max_length=200, default=1)
    book_active = models.BooleanField(default=True)
    book_position_section = models.CharField(max_length=20, choices=SECTION_CHOICES, default=None,)
    book_position_row = models.CharField(max_length=20, choices=ROW_CHOICES, default=None,)
    book_position_rack = models.CharField(max_length=20, choices=RACK_CHOICES, default=None,)
    book_position_rack_level = models.CharField(max_length=20, choices=RACK_LEVEL_CHOICES, default=None,)
    def make_slug(self, book_title):
        slug = book_title.replace(" ", "")
        slug = slug.lower()
        return slug
    def get_date(self):
        return self.modified.date()
    def is_overdue(self):
        if self.book_borrowed:
            duration = timezone.now() - self.book_return_dateline
            if duration > datetime.timedelta(seconds=1):
                return True
            else:
                return False
        else:
            return False
    def can_be_renewed(self):
        if self.book_borrowed:
            duration = self.book_return_dateline - timezone.now()
            if duration < datetime.timedelta(days=5):
                return True
            else:
                return False
        else:
            return False
    def __str__(self):
        return self.book_title
