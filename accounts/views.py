from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth




def signup(request):
    model=User
    if request.method=='POST':
        #The user wants to signup
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.get(username=request.POST['username'])
                return render(request,'register/signup.html',{'error':'Username has already been taken'})
            except User.DoesNotExist:
                user= User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
            try:
                user= User.objects.get(username=request.POST['email'])
                return render(request,'register/signup.html',{'error':'Email ID already exists'})
            except User.DoesNotExist:
                user= User.objects.create_user(request.POST['email'],password=request.POST['password1'])
                auth.login(request,user)
                return redirect('home')
        else:
            return render(request,'register/signup.html',{'error':'Password dosent match'})
    else:
        return render(request,'register/signup.html')

def login(request):
    if request.method=='POST':
        user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            return render(request,'register/login.html',{'error':'username or password is inccorrect'})
    else:
        return render(request,'register/login.html')


def logout(request):
    
    if request.method=='POST':
        auth.logout(request)
        return redirect('logout')
        
    return render(request,'register/logout.html')