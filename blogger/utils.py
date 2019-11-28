import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from .models import *

def send_email(recipient, subject, content):
    message = Mail(
        from_email='blogitweb@gmail.com',
        to_emails=recipient,
        subject=subject,
        html_content=content)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

def is_verified(user, context):
    if not email_verification_token.objects.filter(user=user):
        context['is_verified'] = True
        return True
    context['is_verified'] = False
    return False

def is_authenticated(request, context):
    if request.user.is_authenticated:
        context['is_authenticated'] = True
        context['auth_name'] = request.user.first_name + " " + request.user.last_name
        return True
    context['is_authenticated'] = False
    return False

def get_all_categories(context):
    context['categories'] = category.objects.all

def give_vote(blog, user, liked):
    has_voted = vote.objects.filter(blog=blog, user=user)

    if has_voted:
        return False
    else:
        vote.objects.create(blog=blog, user=user, liked=liked)
        return True

def get_like_percentage(blog, context):
    all_votes = vote.objects.filter(blog=blog)
    liked = vote.objects.filter(blog=blog, liked=True)
    disliked = vote.objects.filter(blog=blog, liked=False)
    if all_votes:
        context['percentage'] = (len(liked)/len(all_votes))*100
    else:
        context['percentage'] = 100

def get_all_blogs(context):
    context['blogs'] = blog.objects.all

def get_category_blogs(category_name, context):
    context['blogs'] = blog.objects.filter(tag=category_name)
    context['category'] = category_name

def get_search_results(search_text, context):
    context['blogs'] = blog.objects.filter(title__icontains=search_text)

def get_top_three_blogs(context):
    context['top_three'] = blog.objects.all().order_by('-date_created')[0:3]