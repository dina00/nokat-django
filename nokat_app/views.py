from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
# from nokat_app.models import
from nokat_app.forms import UserForm
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout  # for later
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.forms import formset_factory
from django.forms import modelformset_factory

# Create your views here.

def register(request):
    registered = False
    if request.method == "POST":
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(user_form.errors)

    else:  # http request
        user_form = UserForm()
    return render(request, 'register.html', {'user_form': user_form,'registered': registered})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print('someone tried to login and failed :(')
            print('username: {} password: {}'.format(username, password))
            return HttpResponse('invalid login details supplied')

    else:
        return render(request, 'login.html', {})


def index(request):
    return render(request, 'index.html')
