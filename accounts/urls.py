
from django.contrib import admin
from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url


urlpatterns = [
    path('signup',views.signup, name='signup'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('profile/',views.bio, name='bio'),

    path('change-password/', views.change_password, name='change_password'),
    url('^', include('django.contrib.auth.urls')),

]    


