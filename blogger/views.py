from django.shortcuts import render

# Create your views here.

def indexView(request):
    return render(request,'index.html')

def logInView(request):
    return render(request,'login.html')

def aboutView(request):
    return render(request,'about.html')

def categoryView(request):
    return render(request,'category.html')

def contactView(request):
    return render(request,'contact.html')

def blogSingleView(request):
    return render(request,'blog-single.html')

def signUpView(request):
    return render(request,'signup.html')