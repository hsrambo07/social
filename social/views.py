from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')