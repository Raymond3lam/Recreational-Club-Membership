from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import models
from .models import Practice, Group, CustomUser
from .forms import ManagePracticeCoachesForm, AddMemberToPracticeForm, PaymentForm, RegisterForm, LoginForm, CreatePracticeForm, AddCoachForm
from django.contrib.auth.decorators import login_required, permission_required

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    context = {
        'title': 'About Page'
    }
    return render(request, 'main/about.html', context)

def practice(request):
    if not (request.user.has_perm('main.add_practice') or request.user.has_perm('main.change_practice')):
        return redirect('home')
    context = {'title': 'Manage Practices'}

    # Treasurer
    if request.user.has_perm('main.add_practice'):
        if request.method == 'POST':
            form1 = CreatePracticeForm(request.POST)
            form2 = ManagePracticeCoachesForm(request.POST)
            if form1.is_valid():
                form1.save()
                return redirect('practice')
            if form2.is_valid():
                form2.save()
                return redirect('practice')
        else:
            form1 = CreatePracticeForm()
            form2 = ManagePracticeCoachesForm()
        context.update({'form1': form1, 'form2': form2}) 
    elif request.user.has_perm('main.change_practice'):
        practices = Practice.objects.filter(coach=request.user)
        for practice in practices:
                practice.form = AddMemberToPracticeForm(instance=practice)
        if request.method == 'POST':
            practice_id = request.POST.get('practice_id')
            practice = practices.get(id=practice_id)
            form = AddMemberToPracticeForm(request.POST, instance=practice)
            if form.is_valid():
                user = form.cleaned_data['members']
                practice.members.add(user)
                return redirect('practice')
        context.update({'practices': practices})

    return render(request, 'main/practice.html', context) 

@permission_required('main.add_payment')
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

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def announcements(request):
    context = {
        'title': 'Club Announcements',
        'announcements': models.Announcement.objects.all()
    }
    return render(request, 'main/announcements.html', context)

@permission_required('main.view_customuser')
def practice_members(request):
    practices = Practice.objects.all()  # Get all Practice objects
    return render(request, 'main/lessons.html', {'practices': practices})

@permission_required('main.manage_coaches')
def manage_coaches(request):
    if request.method == 'POST':
        form = AddCoachForm(request.POST)
        if form.is_valid():
            coach = form.cleaned_data['member']
            coach.groups.add(Group.objects.get(name='Coach'))
            coach.groups.remove(Group.objects.get(name='Member'))
            models.Payment.objects.filter(user=coach).delete()
            return redirect('coach')
    else:
        form = AddCoachForm()

    coaches = models.CustomUser.objects.filter(groups__name='Coach')
    return render(request, 'main/coach.html', {'coaches': coaches, 'form': form})

@permission_required('main.manage_coaches')
def remove_coach(request, id):
    coach = models.CustomUser.objects.get(id=id)
    coach.groups.remove(Group.objects.get(name='Coach'))
    coach.groups.add(Group.objects.get(name='Member'))
    models.Practice.objects.filter(coach=coach).delete()
    return redirect('coach')

@permission_required('main.change_practice')
def remove_member(request, member_id, practice_id):
    practice = Practice.objects.get(id=practice_id)
    member = models.CustomUser.objects.get(id=member_id)
    practice.members.remove(member)
    return redirect('practice')

@permission_required('main.view_customuser')
def get_members(request):
    my_dict = {}
    practices = Practice.objects.all()
    unpaid = 0
    for practice in practices:
        for member in practice.members.all():
            paid = Practice.paid(practice, member)
            if paid:
                unpaid = 0
            else:
                unpaid = 1
            if member in my_dict:
                attendances, unpaid_old = my_dict[member]
                my_dict[member] = (attendances + 1, unpaid_old + unpaid)
            else:
                my_dict[member] = (1, unpaid)
    context = {"members": my_dict}
    return render(request, 'main/lessons.html', context=context)
