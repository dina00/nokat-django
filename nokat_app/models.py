from django.db import models
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.core.validators import MaxLengthValidator

class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,blank=True, null=True)
    content =  models.CharField(max_length=200, validators=[MaxLengthValidator(200, message='max limit exceeded')])
    upvote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="upvotes" ,)
    downvote = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="downvotes" ,)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.content

    def clean_fields(self, exclude=None):
        if len(self.content)>200:
             raise ValidationError(('char limit exceeded.'))

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content =  models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
            return self.content
