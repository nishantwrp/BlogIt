from django.urls import path
from .views import *

urlpatterns = [
    path('', indexView, name='index'),
    path('login/', logInView, name='logIn'),
    path('category/', categoryView, name='category'),
    path('contact/', contactView, name='contact'),
    path('about/', aboutView, name='about'),
    path('blogsingle/', blogSingleView, name='blog-single'),
    path('signup/', signUpView, name='signup')
]