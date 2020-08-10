from django import forms
from django.forms import ValidationError
from django.core import validators
from django.contrib.auth.models import User
# from nokat_app.models import


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username','email','password')
