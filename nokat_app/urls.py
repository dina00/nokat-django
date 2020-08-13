from django.conf.urls import url
from nokat_app import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url


# TEMPLATE TAGGING
app_name= 'nokat_app'
urlpatterns = [
            path('reply/<int:id>', views.reply, name='reply'),
            path('upvote/<int:id>', views.upvote, name='upvote'),
            path('downvote/<int:id>', views.downvote, name='downvote'),
            path('user_profile/<int:id>', views.user_profile, name='user_profile'),
        ]
