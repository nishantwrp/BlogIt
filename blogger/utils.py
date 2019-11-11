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