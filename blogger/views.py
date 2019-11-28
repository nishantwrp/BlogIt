from django.shortcuts import render
from django.contrib.auth import logout
from .forms import *
from .sql import *
from .models import *
from .utils import *
from datetime import datetime

# Create your views here.

def indexView(request):
    context = {}

    get_all_categories(context)
    get_all_blogs(context)
    get_top_three_blogs(context)

    if is_authenticated(request, context):
        is_verified(request.user, context)
    return render(request, 'index.html', context)

def loginView(request):
    context = {}

    get_all_categories(context)

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

    get_all_categories(context)

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

    get_all_categories(context)

    if not is_authenticated(request, context):
        return render(request, 'redirect_home.html', context)

    if is_verified(request.user, context):
        return render(request, 'redirect_home.html', context)

    if request.method == 'POST':
        confirm_form = emailVerificationForm(request.POST)
        if confirm_form.is_valid():

            # Django Query
            correct_token = email_verification_token.objects.get(user=request.user).token

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

def createBlogView(request):
    context = {}

    get_all_categories(context)

    if not ((is_authenticated(request, context)) and (is_verified(request.user, context))):
        return render(request, 'redirect_login.html', context)

    if request.method == 'POST':
        data = request.POST
        title = data['title']
        description = data['description']
        tag = data['tag']
        image = data['image']
        content = data['content']
        if (title == "") or (description == "") or (tag == "") or (image == "") or (content == ""):
            context['toast_message'] = 'fill_all_the_details_correctly'
        else:
            blog_obj = blog.objects.create(author=request.user, title=title, date_created=datetime.now(), description=description, tag=tag, image=image, content=content)

            # Django Query 
            result = category.objects.filter(name=tag)

            if len(result) == 0:
                category.objects.create(name=tag, count=1)
            else:
                obj = category.objects.get(name=tag)
                obj.count += 1
                obj.save()
            
            context['blog_id'] = blog_obj.id
            return render(request, 'redirect_blog.html', context)
            
    return render(request, 'createblog.html', context)

def blogView(request, num):
    context = {}

    get_all_categories(context)

    # Django Query
    result = blog.objects.filter(id=num)

    if len(result) == 0:
        return render(request, 'redirect_home.html', context)

    if is_authenticated(request, context):
        is_verified(request.user, context)

    try:
        if request.GET['vote'] == 'like':
            if not request.user.is_authenticated:
                context['blog_id'] = num
                return render(request, 'redirect_blog_err.html', context)
            if give_vote(blog.objects.get(id=num), request.user, 1):
                context['blog_id'] = num
                return render(request, 'redirect_blog_success.html', context)
            else:
                context['blog_id'] = num
                return render(request, 'redirect_blog_error.html', context)
        elif request.GET['vote'] == 'dislike':
            if not request.user.is_authenticated:
                context['blog_id'] = num
                return render(request, 'redirect_blog_err.html', context)
            if give_vote(blog.objects.get(id=num), request.user, 0):
                context['blog_id'] = num
                return render(request, 'redirect_blog_success.html', context)
            else:
                context['blog_id'] = num
                return render(request, 'redirect_blog_error.html', context)
    except:
        pass

    try:
        if request.GET['err'] == 'true':
            context['toast_message'] = 'should_be_logged_in'
    except:
        pass

    try:
        if request.GET['error'] == 'true':
            context['toast_message'] = 'already_voted'
    except:
        pass

    try:
        if request.GET['success'] == 'true':
            context['toast_message'] = 'vote_recorded'
    except:
        pass
    
    context['blog'] = blog.objects.get(id=num)
    
    get_like_percentage(blog.objects.get(id=num), context)

    return render(request,'blog.html', context)

def categoryView(request, num):
    context = {}

    get_all_categories(context)

    # Django Query
    result = category.objects.filter(id=num)

    if len(result) == 0:
        return render(request, 'redirect_home.html', context)

    get_category_blogs(category.objects.get(id=num).name, context)

    if is_authenticated(request, context):
        is_verified(request.user, context)

    return render(request, 'category.html', context)

def searchView(request):
    context = {}

    get_all_categories(context)

    if request.method == 'POST':
        search_query = request.POST['search_text']
        context['search_query'] = search_query
        get_search_results(search_query, context)
    else:
        return render(request, 'redirect_home.html', context)

    if is_authenticated(request, context):
        is_verified(request.user, context)

    return render(request, 'search.html', context)

def aboutView(request):
    return render(request,'about.html')

def contactView(request):
    return render(request,'contact.html')
