from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import models
from .forms import RegisterForm, LoginForm, PracticeForm

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    context = {
        'title': 'About Page'
    }
    return render(request, 'main/about.html', context)

def practice(request):
    if request.method == 'POST':
        form = PracticeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('some_success_url') 
    else:
        form = PracticeForm()

    context = {
        'title': 'Schedule Practice',
        'form': form  
    }
    return render(request, 'main/practice.html', context) 

def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'main/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request,username=username, password=password)
            if user:
                login(request, user)
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('home')

def announcements(request):
    context = {
        'title': 'Club Announcements',
        'announcements': models.Announcement.objects.all()
    }
    return render(request, 'main/announcements.html', context)