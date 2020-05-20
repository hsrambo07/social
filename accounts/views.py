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
from django.views.generic import FormView
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from accounts.forms import UpdateProfileForm,UserEditForm,ProfileEditForm



def signup(request):
    model=User
    if request.method=='POST':
        #The user wants to signup
        if request.POST['password1'] == request.POST['password2']:
                
                try:
                    user= User.objects.get(username=request.POST['username'])
                    return render(request,'register/signup.html',{'error':'Username has already been taken'})

                except User.DoesNotExist:
                    user= User.objects.create_user(username=request.POST['username'],password=request.POST['password1'],email=request.POST['email'])
                    userprofile = Profile.objects.create(user=user)
                    user.first_name =request.POST['first_name']
                    user.last_name =request.POST['last_name']
                    user.save()
                    auth.login(request,user)
                    response=redirect('edit')
                    return response
        else:
            return render(request,'register/signup.html',{'error':'Password dosent match'})
    else:
        return render(request,'register/signup.html')

def login(request):
    if request.method=='POST':
        user=auth.authenticate(username=request.POST['username'],password=request.POST['password1'])
        if user is not None:
            auth.login(request,user)
            return redirect('edit')
        else:
            return render(request,'registeration/login.html',{'error':'username or password is incorrect'})
    else:
        return render(request,'registration/login.html')


def logout(request):
    
    if request.method=='POST':
        auth.logout(request)
        return render(request,'registration/logout.html')
        
    return render(request,'register/logout.html')


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {
        'form': form
    })    


@login_required

def edit(request):
    if request.method == 'POST':
        user_form=UserEditForm(instance=request.user,data=request.POST)
        profile_form=ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'Profile Updated Successfully')
            response=redirect('view_profile')
            return response
        else:
            messages.error(request,'Error Updating your profile')

    
    else:
        profile = Profile(user=request.user)

        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
        

    return render(request,'accounts/edit.html',{'user_form':user_form,'profile_form':profile_form})    



@login_required
def view_profile(request, pk=None):
    if pk:
        users= get_object_or_404(Profile, pk=pk)
    else:
        users = request.user
    product = {'users': users,'name':request.user.first_name}
    return render(request, 'accounts/profile.html', product)
