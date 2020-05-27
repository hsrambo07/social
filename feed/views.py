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
from django.views .decorators.http import require_POST    
from django.http import JsonResponse


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


@login_required

def post_detail(request,id,slug):
    model = UserPost
    images = UserPost(user=request.user)
    context_object_name = 'post'
    image=get_object_or_404(UserPost,id=id,slug=slug)
    
    return render(request,'post.html',{'section':'images','post':image,'images':images})

@login_required
@require_POST
def post_like(request):
    post_id=request.POST.get('id')
    action=request.POST.get('action')
    if post_id and action:
        try:
            post=UserPost.objects.get(id=post_id)
            if action=="like":
                post.users_like.add(request.user)
            else:
                post.users_like.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'ok'})                


@login_required

def allfeed(request):
    feeds=UserPost.objects.all().order_by('-post_date')
    return render(request,'allfeed.html',{'feeds':feeds})
