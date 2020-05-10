from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.urls import reverse




def signup(request):
    model=User
    if request.method=='POST':
        #The user wants to signup
        if request.POST['password1'] == request.POST['password2']:
                
                try:
                    user= User.objects.get(username=request.POST['username'])
                    return render(request,'register/signup.html',{'error':'Username has already been taken'})

                except User.DoesNotExist:
                    user= User.objects.create_user(request.POST['username'],password=request.POST['password1'],email=request.POST['email'])
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
            return render(request,'registration/login.html',{'error':'username or password is inccorrect'})
    else:
        return render(request,'registration/login.html')


def logout(request):
    
    if request.method=='POST':
        auth.logout(request)
        return render(request,'registration/logout.html')
        
    return render(request,'register/logout.html')



def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })    



@login_required
def edit_profile(request):
    if request.method=='POST':
        if request.POST['name']  and request.POST['last_name'] and request.POST['url'] and request.POST['bio'] and request.FILES['image']:
            product=Profile()
            product.name= request.POST['name']

            product.last_name= request.POST['last_name']

            product.bio= request.POST['bio']
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):        
                product.url= request.POST['url']   
            else:
                product.url= 'http://' + request.POST['url']     
  
            product.image= request.FILES['image']
            product.save()
            return redirect('home')
        else:
            return render(request,'accounts/edit_profile.html',{'error':'Hey,all fields are required'})     
    else:
        return render(request,'accounts/edit_profile.html')



def view_profile(request, pk=None):
    if pk:
        user = detailblog=get_object_or_404(Profile, pk=pk)
    else:
        user = request.user
    product = {'user': user}
    return render(request, 'accounts/profile.html', args)

