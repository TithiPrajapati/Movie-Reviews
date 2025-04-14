from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def signupaccount(request):
    if request.method == 'GET':
        return render(request,'signupaccount.html',{'form':UserCreateForm()})  # Note the parentheses
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')  # Add namespace
            except IntegrityError:
                return render(request,'signupaccount.html',
                {'form':UserCreateForm(),'error':'Username already taken. Choose new username.'})
        else:
            return render(request, 'signupaccount.html',
            {'form':UserCreateForm(),'error':'Passwords do not match'})

def loginaccount(request):
    if request.method == 'GET':
        return render(request,'loginaccount.html',{'form':AuthenticationForm()})  # Note the parentheses
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'loginaccount.html',
            {'form':AuthenticationForm(),'error':'Username and password do not match.'})  # Fixed dictionary
        else:
            login(request,user)
            return redirect('home') 
@login_required 
def logoutaccount(request):
    logout(request)
    return redirect('home')