from django.db import models
from django.utils import timezone

from .book import Book
from .choices import TRANSACTION_TYPE

class TransactionHistory(models.Model):
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE, default=None,)
    book_title = models.ForeignKey(Book)
    book_return_dateline = models.DateTimeField('return dateline', default=None, null=True, blank=False)
    book_returned_date = models.DateTimeField('date returned', default=None, null=True, blank=True)
    book_borrowed_date = models.DateTimeField('date borrowed', default=None, null=True, blank=True)
    book_reserved = models.BooleanField(default=False)
    book_borrowed = models.BooleanField(default=False)
    book_borrowed_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True, related_name="borrowed_user")
    book_reserved_by = models.ForeignKey(User, default=None, on_delete=models.SET_DEFAULT, blank=False, null=True, related_name="reserved_user")
    book_reserved_date = models.DateTimeField('date reserved', default=None, null=True, blank=True)
    book_reservation_end_date = models.DateTimeField('reservation end', default=None, null=True, blank=True)
