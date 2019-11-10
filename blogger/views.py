from django.shortcuts import render
from .forms import *
from .sql import *

# Create your views here.

def indexView(request):
    return render(request,'index.html')

def loginView(request):
    context = {}

    # Logged Out User Only

    if request.method == 'POST':
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            if login_form.verify_credentials_and_login_user(request):
                return render(request,'redirect_confirm.html')
            else:
                context['toast_message'] = 'invalid_credentials'
                return render(request, 'login.html', context)
        else:
            context['toast_message'] = 'invalid_credentials'
            return render(request, 'login.html', context)

    return render(request, 'login.html', context)

def registerView(request):
    context = {}

    # Logged Out User Only

    if request.method == 'POST':
        register_form = registerForm(request.POST)
        if register_form.is_valid():
            if register_form.check_password():
                if register_form.validate_password():
                    if register_form.check_email():
                        if register_form.check_if_username_is_unique():
                            if register_form.check_if_email_is_unique():
                                user = register_form.create_user()
                                register_form.generate_email_verification_token(user)
                                register_form.verify_credentials_and_login_user(request)
                                return render(request,'redirect_confirm.html')
                            else:
                                context['toast_message'] = 'email_already_exists'
                                return render(request, 'register.html', context)
                        else:
                            context['toast_message'] = 'username_already_exists'
                            return render(request, 'register.html', context)
                    else:
                        context['toast_message'] = 'invalid_email'
                        return render(request, 'register.html', context)
                else:
                    context['toast_message'] = 'invalid_password'
                    return render(request, 'register.html', context) 
            else:
                context['toast_message'] = 'passwords_dont_match'
                return render(request, 'register.html', context)
        else:
            context['toast_message'] = 'fill_all_the_details'
            return render(request, 'register.html', context)

    return render(request, 'register.html', context)

def confirmEmailView(request):
    context = {}

    # Logged In Only

    context['email'] = request.user.email

    return render(request, 'confirm_email.html', context)

def aboutView(request):
    return render(request,'about.html')

def categoryView(request):
    return render(request,'category.html')

def contactView(request):
    return render(request,'contact.html')

def blogSingleView(request):
    return render(request,'blog-single.html')
