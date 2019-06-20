from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

from system.models import Book, Notice
from system.forms import AddBookForm#, LendBookForm

def searchbook(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        query = query.strip()
        if query is not None:
            results = Book.objects.filter(Q(book_title__icontains=query) | Q(book_author__icontains=query) |
                                          Q(book_category__book_category__icontains=query) & Q(book_active=True))
            return render(request = request,
                          template_name = 'system/search_results.html',
                          context={'books': results, 'from':'searchbook'})
        else:
            return render(request = request, template_name = 'system/search_results.html')
    else:
        return render(request = request, template_name ='system/search_results.html')

def searchunavbooks(request):
    results = Book.objects.filter(Q(book_borrowed=1) & Q(book_active=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'books': results, 'from':'searchbook'})

def searchrevbooks(request):
    results = Book.objects.filter(Q(book_reserved=1) & Q(book_active=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'books': results, 'from':'searchbook'})

def searchtitleordered(request):
    results = Book.objects.order_by('book_title').filter(Q(book_active=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'books': results, 'from':'searchbook'})

def searchtitlerevordered(request):
    results = Book.objects.order_by('-book_title').filter(Q(book_active=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'books': results, 'from':'searchbook'})

def addbook(request):
    if request.method == "POST":
        form = AddBookForm(request.POST)
        if form.is_valid():
            book = form.save(commit=False)
            book.book_slug = book.make_slug(book.book_title)
            book.save()
            form = AddBookForm()
            messages.success(request, 'Book added.')
            return redirect('system:index')
        else:
            messages.warning(request, 'Book not added')
    else:
        form = AddBookForm()
    return render(request = request,
                  template_name = 'system/form.html',
                  context = {"form":form, "notices":Notice.objects.all(), "from":"addbook"})
# remember the other parameter is linked to urls,
# example: path('<int:book_id>/editbook/', views.editbook, name='editbook'),
def editbook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = AddBookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            messages.success(request, 'Book edited.')
            return redirect('system:index')
    else:
        form = AddBookForm(instance=book)
    return render(request = request,
                  template_name = 'system/form.html',
                  context={'form': form, "notices":Notice.objects.all(), "from":"editbook"})

def returnbook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.book_borrowed and book.book_reserved:
        book.book_reservation_end_date = timezone.now() + datetime.timedelta(days=3)
    if book.is_overdue():
        try:
            borrower = User.objects.get(id=book.book_borrowed_by.id)
        except User.DoesNotExists:
            return redirect("system:index")
        borrower.fine += 20
        borrower.save()
    borrower = User.objects.get(id=book.book_borrowed_by.id)
    borrower.has_borrowed = False
    book.book_return_dateline = None
    book.book_returned_date = timezone.now()
    book.book_borrowed_date = None
    book.book_borrowed = False
    book.book_borrowed_by = None
    book.save()
    messages.success(request, 'Book returned.')
    return redirect("system:index")

def renewbook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if not book.is_overdue() and book.can_be_renewed():
        book.book_return_dateline = book.book_return_dateline  + datetime.timedelta(days=14)
        book.save()
        messages.success(request, 'Book renewed.')
        return redirect("system:index")
    elif book.is_overdue():
        messages.error(request, f'Book is overdue, please return and settle any outstanding fine. {book.is_overdue}')
        return redirect("system:index")
    elif not book.can_be_renewed():
        messages.error(request, 'Book can only be renewed after being borrowed more than a week.')
        return redirect("system:index")
    else:
        messages.error(request, 'Book not renewed')
        return redirect("system:index")

def removebook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.book_active = False
    book.book_borrowed = False
    book.book_reserved = False
    book.save()
    return render(request = request,
                  template_name = 'system/index.html',
                  context = {"books": Book.objects.all(), "notices":Notice.objects.all()})

def reservebook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.book_reserved = True
    book.book_reserved_by = request.user
    book.book_reserved_date = timezone.now()
    book.save()
    return render(request = request,
                  template_name = 'system/index.html',
                  context = {"books": Book.objects.all(), "notices":Notice.objects.all()})

def unreservebookfunc(book):
    book.book_reserved_by = None
    book.book_reserved_date = None
    book.book_reservation_end_date = None
    book.book_reserved = False

def unreservebook(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if book.book_reserved:
        unreservebookfunc(book)
    book.save()
    return render(request = request,
                  template_name = 'system/index.html',
                  context = {"books": Book.objects.all(), "notices":Notice.objects.all()})

def lendbook(request, book_id):
    # book = get_object_or_404(Book, id=book_id)
    # if request.method == "POST":
    #     form = LendBookForm(request.POST, instance=book)
    #     if form.is_valid():
    #         book = form.save(commit=False)
    #         book.book_borrowed_date = timezone.now()
    #         book.book_return_dateline = timezone.now() + datetime.timedelta(days=14)
    #         book.book_borrowed = True
    #         if book.book_reserved:
    #             unreservebookfunc(book)
    #         book.save()
    #         messages.success(request, 'Book lent.')
    #         return redirect('system:index')
    # else:
    #     form = LendBookForm(instance=book)
    return render(request = request,
                  template_name = 'system/form.html',
                  context={'form': form, "notices": Notice.objects.all(), "from":"lendbook", 'book': book})
