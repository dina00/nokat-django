from django.conf.urls import url
from nokat_app import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url


# TEMPLATE TAGGING
app_name= 'nokat_app'
urlpatterns = [
            path('reply/<int:id>', views.reply, name='reply'),
            path('joke_delete/<int:id>', views.joke_delete, name='joke_delete'),
            path('upvote/<int:id>', views.upvote, name='upvote'),
            path('downvote/<int:id>', views.downvote, name='downvote'),
            path('user_profile/<int:id>', views.user_profile, name='user_profile'),
            path('least_recent_posts/', views.least_recent_posts, name='least_recent_posts'),
            path('most_popular_posts/', views.most_popular_posts, name='most_popular_posts'),
            path('least_popular_posts/', views.least_popular_posts, name='least_popular_posts'),
            path('recent_activity_posts/', views.recent_activity_posts, name='recent_activity_posts'),
            path('oldest_activity_posts/', views.oldest_activity_posts, name='oldest_activity_posts'),
            path('search/', views.search, name='search'),
    #'feed/' being the name of desired url, 'views.search' the
    #name of your func-based view, and "name='home'" the template
    #you're using.
]
