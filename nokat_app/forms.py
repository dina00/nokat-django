from django import forms
from django.forms import ValidationError
from django.core import validators
from django.contrib.auth.models import User
from nokat_app.models import Post, Comment


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')

class FormPost(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('content',)
        widgets = {
            'content': forms.TextInput(attrs={
                'id': 'post-text',
                'required': True,
                'placeholder': 'Say something...'
            }),
            }

class FormComment(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('content',)
