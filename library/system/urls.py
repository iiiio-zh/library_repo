from django.urls import path

from . import views

app_name = 'system'
urlpatterns = [
    path('', views.index, name='index'),
    path('searchbook/', views.searchbook, name='searchbook'),
    path('searchunavbooks/', views.searchunavbooks, name='searchunavbooks'),
    path('searchrevbooks/', views.searchrevbooks, name='searchrevbooks'),
    path('searchtitleordered/', views.searchtitleordered, name='searchtitleordered'),
    path('searchtitlerevordered/', views.searchtitlerevordered, name='searchtitlerevordered'),
    path('searchuser/', views.searchuser, name='searchuser'),
    path('searchuserordered/', views.searchuserordered, name='searchuserordered'),
    path('searchuserrevordered/', views.searchuserrevordered, name='searchuserrevordered'),
    path('searchuserbr/', views.searchuserbr, name='searchuserbr'),
    path('addbook/', views.addbook, name='addbook'),
    path('<int:book_id>/editbook/', views.editbook, name='editbook'),
    path('<int:book_id>/removebook/', views.removebook, name='removebook'),
    path('<int:book_id>/returnbook/', views.returnbook, name='returnbook'),
    path('<int:book_id>/lendbook/', views.lendbook, name='lendbook'),
    path('<int:book_id>/reservebook/', views.reservebook, name='reservebook'),
    path('<int:book_id>/unreservebook/', views.unreservebook, name='unreservebook'),
    path('<int:book_id>/renewbook/', views.renewbook, name='renewbook'),
    path('<int:user_id>/userprofile/', views.viewuser, name='viewuser'),
    path('adduser/', views.adduser, name='adduser'),
    path('login', views.login_request, name='login'),
    path('logout', views.logout_request, name='logout'),
]
