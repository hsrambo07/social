from . import views
from django.conf.urls import url
from django.contrib import admin
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns




urlpatterns=[
    path('create/',views.post_create,name='create'),
    path('create/<int:id>/<slug:slug>/',views.post_detail,name='detail'),
    path('like/',views.image_like,name='like'),
    path('allfeeds/',views.allfeed,name='feed'),

]