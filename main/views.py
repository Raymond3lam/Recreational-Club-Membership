from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import models
from .models import Practice
from .forms import PaymentForm, RegisterForm, LoginForm, PracticeForm

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
            return redirect('practice')
    else:
        form = PracticeForm()

    context = {
        'title': 'Schedule Practice',
        'form': form  
    }
    return render(request, 'main/practice.html', context) 

def payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('payment')
    else:
        form = PaymentForm(user=request.user)
    
    context = {
        'title': 'Make Payment',
        'form': form
    }
    return render(request, 'main/payment.html', context)

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

def practice_members(request):
    practices = Practice.objects.all()  # Get all Practice objects
    return render(request, 'main/lessons.html', {'practices': practices})
