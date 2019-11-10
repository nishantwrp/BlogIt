from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class email_verification_token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.username}'