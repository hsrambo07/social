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
from feed.models import UserPost
from django.views .decorators.http import require_POST   
from django.http import JsonResponse
from django.views import generic
from common.decorators import ajax_required
from django.http import HttpResponse
from django.http import HttpResponseBadRequest



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
    uploads=UserPost.objects.filter(user=request.user)
    product = {'users': users,'name':request.user.first_name,'content':uploads}
    return render(request, 'accounts/profile.html', product)

@login_required
def user_list(request):
    users=User.objects.filter(is_active=True)
    return render(request,'accounts/list.html',{'section':'people','users':users})

@login_required
def user_detail(request,username):
    user=get_object_or_404(User,username=username,is_active=True)
    upload=UserPost.objects.filter(user=user.id)
    return render(request,'accounts/detail.html',{'section':'people','user':user,'content':upload})

@ajax_required
@login_required
@require_POST
def user_follow(request):
    user_id=request.POST.get('id')
    action=request.POST.get('action')
    if user_id and action:
        try:
            user= User.objects.get(id=user_id)
            if action=='follow':
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})        


class UserFollow(generic.RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        pk = self.kwargs.get('pk')

        celeb = get_object_or_404(User, pk=pk)
        url_ = celeb.get_absolute_url()

        if self.request.user.is_authenticated:
            if self.request.user in celeb.followers.all():
                Contact.objects.filter(user_from=self.request.user,
                                       user_to=celeb).delete()
            else:
                Contact.objects.get_or_create(user_from=self.request.user,
                                              user_to=celeb)
                create_action(self.request.user, 'is now following', celeb)
        return url_

