from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name='index'),
    path('login/', loginView, name='login'),
    path('register/', registerView, name='register'),
    path('logout/', logoutView, name='logout'),
    path('confirm/', confirmEmailView, name='confirm'),
    path('create/', createBlogView, name='createblog'),
    path('blog/<int:num>/', blogView, name='blog'),
    path('category/<int:num>/', categoryView, name='category'),
    path('search/', searchView, name='search'),
    path('about/', aboutView, name='about'),
]