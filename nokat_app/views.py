from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import HttpResponse
from . import forms
from nokat_app.models import Post, Comment
from nokat_app.forms import UserForm, FormPost, FormComment
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
    # access the number of upvotes associated with a post using 'number_of_upvotes' attribute
    posts = Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True))
    if request.method == "POST":
        post_form = FormPost(data=request.POST)
        if post_form.is_valid():
            post_obj=post_form.save(commit=False)
            post_obj.user=request.user
            post_obj.save()
            messages.add_message(request, messages.SUCCESS,'Joke was added successfully')
            return redirect('index')
        else:
            print(post_form.errors)
    else:  # http request
        post_form = FormPost()
    return render(request, 'index.html', {'post_form': post_form,'posts': posts,})

def reply(request, id):
    # get replies of this post
    replies = Comment.objects.filter(post=id)
    post = get_object_or_404(Post, id=id)
    if request.method == "POST":
        comment_form = FormComment(request.POST)
        if comment_form.is_valid():
            comment_obj=comment_form.save(commit=False)
            comment_obj.user=request.user
            comment_obj.post=post
            comment_obj.save()
            messages.add_message(request, messages.SUCCESS,'You replied!')
            return redirect('nokat_app:reply',id)
        else:
            print(comment_form.errors)
    else:  # http request
        comment_form = FormComment()
    return render(request, 'replies.html', {'post': post,'comment_form': comment_form, 'replies': replies})

def upvote(request,id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user.is_authenticated:
        if user in post.upvote.all():
            # you  remove the user if double upvote
            post.upvote.remove(user)
        else:
            post.upvote.add(user)

    return redirect('index')


def downvote(request,id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user.is_authenticated:
        if user in post.downvote.all():
            post.downvote.remove(user)
        else:
            post.downvote.add(user)

    return redirect('index')


def user_profile(request, id):
    posts=Post.objects.filter(user__id=id).annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True))

    return render(request, 'user_profile.html', {'posts': posts})
