from django.shortcuts import render
from django.contrib.auth import logout
from .forms import *
from .sql import *
from .models import *
from .utils import *

# Create your views here.

def indexView(request):
    context = {}

    if is_authenticated(request, context):
        is_verified(request.user, context)
    return render(request, 'index.html', context)

def loginView(request):
    context = {}

    if is_authenticated(request, context):
        return render(request, 'redirect_confirm.html', context)

    if request.method == 'POST':
        login_form = loginForm(request.POST)
        if login_form.is_valid():
            if login_form.verify_credentials_and_login_user(request):
                return render(request,'redirect_confirm.html')
            else:
                context['toast_message'] = 'invalid_credentials'
        else:
            context['toast_message'] = 'invalid_credentials'

    return render(request, 'login.html', context)

def registerView(request):
    context = {}

    if is_authenticated(request, context):
        return render(request, 'redirect_confirm.html', context)

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
                        else:
                            context['toast_message'] = 'username_already_exists'
                    else:
                        context['toast_message'] = 'invalid_email'
                else:
                    context['toast_message'] = 'invalid_password'
            else:
                context['toast_message'] = 'passwords_dont_match'
        else:
            context['toast_message'] = 'fill_all_the_details'

    return render(request, 'register.html', context)

def confirmEmailView(request):
    context = {}

    if not is_authenticated(request, context):
        return render(request, 'redirect_home.html', context)

    if is_verified(request.user, context):
        return render(request, 'redirect_home.html', context)

    if request.method == 'POST':
        confirm_form = emailVerificationForm(request.POST)
        if confirm_form.is_valid():
            # Mysql Query
            query = "select * from blogger_email_verification_token where user_id='{}'".format(request.user.id)
            result = execute_sql_query(query)
            correct_token = result[0][1]

            # Django Query
            # correct_token = email_verification_token.objects.get(user=request.user).token

            if correct_token == confirm_form.cleaned_data['token']:
                confirm_form.verify_email(request.user)
                return render(request, 'redirect_home.html', context)
            else:
                context['toast_message'] = 'invalid_code'
        else:
            context['toast_message'] = 'invalid_code'       

    context['email'] = request.user.email

    return render(request, 'confirm_email.html', context)

def logoutView(request):
    context = {}
    if request.user.is_authenticated:
        logout(request)
    return render(request, 'redirect_home.html', context)

def aboutView(request):
    return render(request,'about.html')

def categoryView(request):
    return render(request,'category.html')

def contactView(request):
    return render(request,'contact.html')

def blogSingleView(request):
    return render(request,'blog-single.html')
