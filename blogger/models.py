from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class email_verification_token(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.username}'

class blog(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateField()
    title = models.CharField(max_length=256)
    description = models.TextField()
    tag = models.CharField(max_length=256)
    image = models.CharField(max_length=256)
    content = models.TextField()

    def __str__(self):
        return f'{self.title} by {self.author.first_name} {self.author.last_name}'

class category(models.Model):
    name = models.CharField(max_length=256)
    count = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.name}'

class vote(models.Model):
    blog = models.ForeignKey(blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField()

    def __str__(self):
        return f'{self.blog}'