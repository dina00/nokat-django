from django.shortcuts import render, redirect
from django.db.models import Count
from django.http import HttpResponse
from . import forms
from nokat_app.models import Post, Comment
from nokat_app.forms import UserForm, FormPost, FormComment
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout  # for later
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
import json
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

@login_required(login_url='/user_login/')
def index(request):
    # access the number of upvotes associated with a post using 'number_of_upvotes' attribute
    posts = Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True))
    # most_recent=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).order_by('-timestamp')
    if request.method == "POST":
        response_data = {}
        post_form = FormPost(data=request.POST)
        if post_form.is_valid():
            post_obj=post_form.save(commit=False)
            post_obj.user=request.user
            post_obj.save()
            messages.add_message(request, messages.SUCCESS,'Joke was added successfully')
        else:
            print(post_form.errors)
    else:  # http request
        post_form = FormPost()
    context={
            'post_form': post_form,
            'posts': posts,
            # 'most_recent':most_recent,
             }
    return render(request, 'index.html', context)

@login_required(login_url='/user_login/')
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
            post.updated_date = timezone.now()
            comment_obj.save()
            post.save()
            messages.add_message(request, messages.SUCCESS,'You replied!')
            return redirect('nokat_app:reply',id)
        else:
            print(comment_form.errors)
    else:  # http request
        comment_form = FormComment()
    return render(request, 'replies.html', {'post': post,'comment_form': comment_form, 'replies': replies})

@login_required(login_url='/user_login/')
def upvote(request,id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user.is_authenticated:
        if user in post.upvote.all():
            # you  remove the user if double upvote
            post.upvote.remove(user)
        else:
            post.upvote.add(user)
        post.updated_date = timezone.now()
        post.save()

    return redirect('index')


@login_required(login_url='/user_login/')
def downvote(request,id):
    post = get_object_or_404(Post, id=id)
    user = request.user
    if user.is_authenticated:
        if user in post.downvote.all():
            post.downvote.remove(user)
        else:
            post.downvote.add(user)
        post.updated_date = timezone.now()
        post.save()

    return redirect('index')


@login_required(login_url='/user_login/')
def user_profile(request, id):
    posts=Post.objects.filter(user__id=id).annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True))

    return render(request, 'user_profile.html', {'posts': posts})

@login_required(login_url='/user_login/')
def most_recent_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).order_by('-timestamp')

    return render(request, 'index.html', {'posts': posts,})

@login_required(login_url='/user_login/')
def least_recent_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).order_by('-timestamp')
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

    return render(request, 'index.html', {'posts': posts,'post_form': post_form})


@login_required(login_url='/user_login/')
def most_popular_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).annotate(like_diff=Count('upvote')-Count('downvote')).order_by('like_diff')
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

    return render(request, 'index.html', {'posts': posts,'post_form': post_form})

@login_required(login_url='/user_login/')
def least_popular_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).annotate(like_diff=Count('upvote')-Count('downvote')).order_by('-like_diff')
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

    return render(request, 'index.html', {'posts': posts,'post_form': post_form})

@login_required(login_url='/user_login/')
def most_popular_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).annotate(like_diff=Count('upvote')-Count('downvote')).order_by('like_diff')
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

    return render(request, 'index.html', {'posts': posts,'post_form': post_form})

@login_required(login_url='/user_login/')
def recent_activity_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).order_by('updated_date')
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

    return render(request, 'index.html', {'posts': posts,'post_form': post_form})

@login_required(login_url='/user_login/')
def oldest_activity_posts(request):
    posts=Post.objects.annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True)).order_by('-updated_date')
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

    return render(request, 'index.html', {'posts': posts,'post_form': post_form})


@login_required(login_url='/user_login/')
def joke_delete(request, id):
    instance = get_object_or_404(Post, id=id)
    instance.delete()
    messages.add_message(request, messages.SUCCESS,'Joke was deleted successfully')
    return redirect('index')


@login_required(login_url='/user_login/')
def search(request):
    search_term=request.GET.get('search_term','')
    posts=Post.objects.filter(content__icontains=search_term).all()
    users=User.objects.filter(username__icontains=search_term).all()
    context={
    'posts':posts,
    'users':users,
    'search_term':search_term,
    }
    return render(request, 'search_results.html', context)


@login_required(login_url='/user_login/')
def list_users(request):
    users=User.objects.all()
    votes_dict={}
    for user in users:
        posts=Post.objects.filter(user=user).annotate(number_of_upvotes=Count('upvote',distinct=True)).annotate(number_of_downvotes=Count('downvote',distinct=True))
        count=0 #reset after every user
        for post in posts:
            diff=post.number_of_upvotes-post.number_of_downvotes
            count+=diff
        votes_dict[user.username]=count

    return render(request, 'list_users.html', {'users':users,'votes_dict':votes_dict})
