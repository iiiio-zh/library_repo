
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone

# from .forms import NewUserForm
from .models import Notice, Book, BookCategory, User
from .forms import AddBookForm, LendBookForm, UserAdminCreationForm

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        return render(request = request,
                      template_name = 'system/index.html',
                      context = {"books":Book.objects.all()[:5], "notices":Notice.objects.all()[:5], "from":"index"})
    else:
        return redirect("system:login")

def account(request):
    return render(request = request, template_name = 'system/account.html')

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

def searchuserordered(request):
    results = User.objects.order_by('first_name').filter(Q(member=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'users': results, 'from':'searchuser'})

def searchuserrevordered(request):
    results = User.objects.order_by('-first_name').filter(Q(member=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'users': results, 'from':'searchuser'})

def searchuserbr(request):
    results = User.objects.order_by('-first_name').filter(Q(member=True))
    return render(request = request,
                  template_name = 'system/search_results.html',
                  context={'users': results, 'from':'searchuser'})

def searchuser(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        if query is not None:
            results = User.objects.filter(Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
            book_borrowed_list = Book.objects.filter(Q(book_borrowed=True))
            return render(request = request,
                          template_name = 'system/search_results.html',
                          context={'users': results, 'booklist': book_borrowed_list, 'from':'searchuser', 'query': query})
        else:
            return render(request = request, template_name = 'system/search_results.html')
    else:
        return render(request = request, template_name ='system/search_results.html')

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
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = LendBookForm(request.POST, instance=book)
        if form.is_valid():
            book = form.save(commit=False)
            book.book_borrowed_date = timezone.now()
            book.book_return_dateline = timezone.now() + datetime.timedelta(days=14)
            book.book_borrowed = True
            if book.book_reserved:
                unreservebookfunc(book)
            book.save()
            messages.success(request, 'Book lent.')
            return redirect('system:index')
    else:
        form = LendBookForm(instance=book)
    return render(request = request,
                  template_name = 'system/form.html',
                  context={'form': form, "notices": Notice.objects.all(), "from":"lendbook", 'book': book})

def adduser(request):
    if request.method == "POST":
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.member = True
            user.save()
            form = UserAdminCreationForm()
            messages.success(request, f'User {user.first_name} {user.last_name} added.')
            return redirect('system:index')
        else:
            messages.warning(request, 'User not added')
    else:
        form = UserAdminCreationForm()
    return render(request = request,
                  template_name = 'system/form.html',
                  context = {"form":form, "notices":Notice.objects.all(), "from":"adduser"})

def viewuser(request, user_id):
    user_viewed = get_object_or_404(User, id=user_id)
    book_borrowed_list = Book.objects.filter(Q(book_borrowed=1) & Q(book_borrowed_by=user_id))
    return render(request = request,
                  template_name = 'system/userprofile.html',
                  context={'user_viewed': user_viewed, "books":book_borrowed_list})

def login_request(request):
    if request.method == "POST":
        form =  AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # messages.info(request, f"You are now logged in as {username}")
                return redirect("system:index")
            else:
                messages.errror(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request = request,
                  template_name = "system/login.html",
                  context={"form":form})

# @login_required
def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("system:index")
