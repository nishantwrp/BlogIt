from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name='index'),
    path('login/', loginView, name='login'),
    path('register/', registerView, name='register'),
    path('logout/', logoutView, name='logout'),
    path('confirm/', confirmEmailView, name='confirm'),
    path('category/', categoryView, name='category'),
    path('contact/', contactView, name='contact'),
    path('about/', aboutView, name='about'),
    path('blogsingle/', blogSingleView, name='blog-single'),
]