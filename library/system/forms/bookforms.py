from django import forms
from django.utils import timezone

from system.models.book import Book

class AddBookForm(forms.ModelForm):
    book_published_date = forms.DateField(required = False, widget=forms.SelectDateWidget(years=range(1300, 2100)))
    class Meta():
        model = Book
        fields = ('book_title', 'book_author', 'book_category', 'book_summary', 'book_published_date',
                  'book_position_section', 'book_position_row', 'book_position_rack',
                  'book_position_rack_level')

# class LendBookForm(forms.ModelForm):
#     class Meta():
#         model = Book
#         # fields = ('book_borrowed_by',)
