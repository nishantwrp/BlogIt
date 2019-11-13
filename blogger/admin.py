from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(email_verification_token)
admin.site.register(blog)
admin.site.register(category)
admin.site.register(vote)