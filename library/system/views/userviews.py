from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages


from system.forms import UserAdminCreationForm
from system.models import Book, User, Notice

def account(request):
    return render(request = request, template_name = 'system/account.html')

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
