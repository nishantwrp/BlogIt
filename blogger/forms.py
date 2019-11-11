from django import forms
from django.contrib.auth import authenticate, login, logout
from validate_email import validate_email
from django.contrib.auth.models import User
from .models import *
from random import randint
from .utils import *

class loginForm(forms.Form):
    username = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256)

    def verify_credentials_and_login_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

class registerForm(forms.Form):
    first_name = forms.CharField(max_length=256)
    last_name = forms.CharField(max_length=256)
    email = forms.CharField(max_length=256)
    username = forms.CharField(max_length=256)
    password = forms.CharField(max_length=256)
    confirm_password = forms.CharField(max_length=256)

    def check_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password == confirm_password:
            return True
        return False

    def validate_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6:
            return False
        return True

    def check_email(self):
        email = self.cleaned_data['email']
        is_valid = validate_email(email)
        return is_valid

    def check_if_username_is_unique(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            return False
        return True

    def check_if_email_is_unique(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            return False
        return True

    def create_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        first_name = self.cleaned_data['first_name']
        last_name = self.cleaned_data['last_name']

        user = User.objects.create_user(username=username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()

        return user
        
    def generate_email_verification_token(self, user):
        random_token = randint(1000,9999)
        email_verification_token.objects.create(user=user, token=random_token)
        send_email(user.email, "Blogit Email Verification Code", f'Hi {user.first_name},<br>Your email verification code is <b>{random_token}</b><br>Regards<br>Blogit')

    def verify_credentials_and_login_user(self, request):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return True
        else:
            return False

class emailVerificationForm(forms.Form):
    token = forms.CharField(max_length=10)

    def verify_email(self, user):
        email_verification_token.objects.filter(user=user).delete()
