from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from system.models import Book, Notice

def index(request):
    if request.user.is_authenticated:
        return render(request = request,
                      template_name = 'system/index.html',
                      context = {"books":Book.objects.all()[:5], "notices":Notice.objects.all()[:5], "from":"index"})
    else:
        return redirect("system:login")
