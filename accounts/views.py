from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Profile



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
        return redirect('logout')
        
    return render(request,'registration/logout.html')



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
def bio(request):
    if request.method=='POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon']  and request.FILES['image']:
            product=Product()
            product.title= request.POST['title']
            product.body= request.POST['body']
            if request.POST['url'].startswith('https://') or request.POST['url'].startswith('http://'):        
                product.url= request.POST['url']   
            else:
                product.url= 'http://' + request.POST['url']     
            product.icon= request.FILES['icon']
            product.image= request.FILES['image']
            product.pub_date=timezone.datetime.now()
            product.hunter =request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request,'bio/bio.html',{'error':'Hey,all fields are required'})     
    else:
        return render(request,'bio/bio.html')

def detail(request,id):
    product= get_object_or_404(Product, pk=id)
    return render(request,'detail.html',{'product':product})