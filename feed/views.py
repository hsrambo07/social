from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserPost
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from feed.forms import UpdateFeedForm
    

@login_required
def post_create(request):
    model=UserPost

    if request.method=='POST':
        
        form = UpdateFeedForm(data=request.POST,files=request.FILES)
        #The user wants to signup                
        if form.is_valid():
            cd=form.cleaned_data
          
            new_item=form.save(commit=False)
            new_item.user=request.user
            new_item.save()
            form.save()
            messages.success(request,'Successfully uploaded')
            return redirect(new_item.get_absolute_url())
    else:
        form=UpdateFeedForm(data=request.GET)
    return render(request,'feed.html',{'form':form})



def post_detail(request,id,slug):
    model = UserPost
    images = UserPost(user=request.user)
    context_object_name = 'post'
    image=get_object_or_404(UserPost,id=id,slug=slug)
    
    return render(request,'post.html',{'section':'images','post':image,'images':images})