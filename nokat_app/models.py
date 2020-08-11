from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    content =  models.CharField(max_length=200)
    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvotes" ,)
    downvote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="downvotes" ,)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.content

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content =  models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.content
