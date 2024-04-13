from calendar import monthrange
from datetime import date, timedelta
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from . import models 
from django.http import HttpResponse
from django.db.models import Q
from .models import Practice, Group, Payment, CustomUser
from .forms import ExpenseForm, ManagePracticeCoachesForm, AddMemberToPracticeForm, PaymentForm, RegisterForm, LoginForm, CreatePracticeForm, AddCoachForm, AnnouncementForm, UpdateAnnouncementForm
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Sum
from django.contrib import messages
# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def about(request):
    context = {
        'title': 'About Page'
    }
    return render(request, 'main/about.html', context)

def add_announcement(request):
    if request.method == 'POST':
        form = AnnouncementForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('announcements')
    else:
        form = AnnouncementForm(user=request.user)
    return render(request, 'main/add_announcement.html', {'form': form})

# @permission_required('main.change_practice')
def coach_practice(request):
    context = {'title': 'Manage Practices'}

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
            announcement = models.Announcement(
                title='Added to practice',
                content=f'You have been added to practice: {practice.name}',
                author=models.CustomUser.objects.get(username='admin'),
            )
            announcement.save()
            target_users = models.CustomUser.objects.filter(username=user.username)
            announcement.target.set(target_users)
            return redirect('coach_practice')
    context.update({'practices': practices})

    return render(request, 'main/coach_practice.html', context) 

@permission_required('main.add_practice')
def treasurer_practice(request):
    context = {'title': 'Manage Practices'}
    practices = Practice.objects.all()
    form = CreatePracticeForm()

    if request.method == 'POST':
        form = CreatePracticeForm(request.POST)
    if form.is_valid():
        practice = form.save()
        announcement = models.Announcement(
            title='Practice Created',
            content=f'Practice: {practice.name} has been created.',
            author=models.CustomUser.objects.get(username='admin'),
        )
        announcement.save()
        target_users = models.CustomUser.objects.filter(username=practice.coach.username)
        announcement.target.set(target_users)
        expense = models.Expense(
            amount=50,
            due=practice.date + timedelta(weeks=2),
            notes=f'Practice: {practice.name} id: {practice.id}',
            category='Coach',
        )
        expense.save()
        return redirect('treasurer_practice')
    else:
        form = CreatePracticeForm()

    for practice in practices:
        practice.form = ManagePracticeCoachesForm(instance=practice)
    if request.method == 'POST':
        practice = Practice.objects.get(id=request.POST.get('practice_id'))
        old_coach = practice.coach
        form = ManagePracticeCoachesForm(request.POST, instance=practice)
        if form.is_valid():
            practice = form.save()
            announcement = models.Announcement(
                title='Removed from practice',
                content=f'You have been removed from practice: {practice.name}',
                author=models.CustomUser.objects.get(username='admin'),
            )
            announcement.save()
            target_users = models.CustomUser.objects.filter(username=old_coach.username)
            announcement.target.set(target_users)

            announcement = models.Announcement(
                title='Assigned to practice',
                content=f'You have been assigned to practice: {practice.name}',
                author=models.CustomUser.objects.get(username='admin'),
            )
            announcement.save()
            target_users = models.CustomUser.objects.filter(username=practice.coach.username)
            announcement.target.set(target_users)
            return redirect('treasurer_practice')
    context.update({'practices': practices, 'form': form })
    return render(request, 'main/treasurer_practice.html', context)

def delete_practice(request, id):
    practice = Practice.objects.get(id=id)
    announcement = models.Announcement(
        title='Practice Removed',
        content=f'Practice: {practice.name} has been removed.',
        author=models.CustomUser.objects.get(username='admin'),
    )
    announcement.save()
    target_users = models.CustomUser.objects.filter(username=practice.coach.username)
    for member in practice.members.all():
        target_users |= models.CustomUser.objects.filter(username=member.username)
    announcement.target.set(target_users)
    expense = models.Expense.objects.filter(notes=f'Practice: {practice.name} id: {practice.id}')
    expense.delete()
    practice.delete()
    return redirect('treasurer_practice')


@permission_required('main.add_payment')
def payment(request):
    amount = 10
    # discount if top ten most attended users
    top_ten = CustomUser.objects.filter(groups__name='Member').exclude(is_superuser=True).annotate(practice_count=Sum('member_practices')).order_by('-practice_count')[:10]
    if request.user in top_ten:
        amount = amount - amount*0.1
    # check all classes attended within last 3 months 
    three_months_ago = date.today() - timedelta(days=90)
    practices = Practice.objects.filter(date__gte=three_months_ago)
    good_three = True
    for practice in practices:
        if not practice.paid(request.user):
            good_three = False
            break
    if good_three:
        amount = amount - amount*0.1
    else:
        amount = amount + amount*0.2
    if request.method == 'POST':
        form = PaymentForm(request.POST, user=request.user)
        if form.is_valid():
            payment = form.save()
            announcement = models.Announcement(
                title='Payment Received',
                content=f'{request.user.username} ({request.user.get_full_name()}) has paid for practice: {payment.practice.name} for ${payment.amount} on {payment.date}.',
                author=models.CustomUser.objects.get(username='admin'),
            )
            announcement.save()
            target_users = models.CustomUser.objects.filter(groups__name='Treasurer') | models.CustomUser.objects.filter(username=payment.practice.coach.username)
            announcement.target.set(target_users)
            return redirect('payment')
    else:
        form = PaymentForm(user=request.user)
    
    context = {
        'title': 'Make Payment',
        'form': form,
        'amount': amount
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
                messages.error(request, 'Invalid username or password')
                
    else:
        form = LoginForm()
    return render(request, 'main/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

def announcements(request):
    user = request.user
    practices = Practice.objects.filter(members=user)
    announcements = models.Announcement.objects.filter(Q(target=user) | Q(target_practices__in=practices) | Q(author=user)).distinct().order_by('-date_updated')
    context = {
        'title': 'Club Announcements',
        'announcements': announcements
    }
    return render(request, 'main/announcements.html', context)

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
    announcement = models.Announcement(
        title='Removed from practice',
        content=f'You have been removed from practice: {practice.name}',
        author=models.CustomUser.objects.get(username='admin'),
    )
    announcement.save()
    target_users = models.CustomUser.objects.filter(username=member.username)
    announcement.target.set(target_users)
    return redirect('coach_practice')

def delete_announcement(request, id):
    if models.Announcement.objects.get(id=id).author == request.user:
        announcement = models.Announcement.objects.get(id=id)
        announcement.delete()
        return redirect('announcements')
    else:
        return redirect('announcements')
    
def update_announcement(request,id):
    if models.Announcement.objects.get(id=id).author == request.user:
        announcement = models.Announcement.objects.get(id=id)
        if request.method == 'POST':
            form = UpdateAnnouncementForm(request.POST, instance=announcement)
            if form.is_valid():
                form.save()
                return redirect('announcements')
        else:
            form = UpdateAnnouncementForm(instance=announcement)
        return render(request, 'main/update_announcement.html', {'form': form})
    else:
        return redirect('announcements')
    
def finances(request):
    today = date.today()
    first_day_next_month = today.replace(day=1, month=today.month+1)

    total_member_payments = Payment.objects.filter(
        Q(date__lte=first_day_next_month) &
        Q(date__gte=today.replace(day=1))
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_revenue = total_member_payments

    total_coach_expenses = models.Expense.objects.filter(
        Q(category='Coach') & 
        Q(due__lte=first_day_next_month) & 
        Q(paid=False)
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_hall_expenses = models.Expense.objects.filter(
        Q(category='Hall') &
        Q(due__lte=first_day_next_month) &
        Q(paid=False)
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_other_expenses = models.Expense.objects.filter(
        Q(category='Other') &
        Q(due__lte=first_day_next_month) &
        Q(paid=False)
    ).aggregate(total=Sum('amount'))['total'] or 0
    total_expenses = total_hall_expenses + total_other_expenses + total_coach_expenses
    income = total_revenue - total_expenses
    context = {
        'title': 'Club Finances',
        'month': today.strftime('%B'),
        'total_member_payments': total_member_payments,
        'total_revenue': total_revenue,
        'total_coach_expenses': total_coach_expenses,
        'total_hall_expenses': total_hall_expenses,
        'total_other_expenses': total_other_expenses,
        'total_expenses': total_expenses,
        'net_income': income
    }
    return render(request, 'main/finances.html', context)

@permission_required('main.view_customuser')
def members(request):
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
    for member in CustomUser.objects.all().filter(groups__name='Member').exclude(is_superuser=True):
        if member not in my_dict:
            my_dict[member] = (0, 0)
        
    context = {"members": my_dict}
    return render(request, 'main/members.html', context=context)

@permission_required('main.manage_finances')
def expenses(request):
    form = ExpenseForm()
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('expenses')
    else:
        form = ExpenseForm()

    expenses = models.Expense.objects.filter(paid=False).order_by('due')
    context = {
        'title': 'Club Expenses',
        'expenses': expenses,
        'form': form
    }
    return render(request, 'main/expenses.html', context)

def pay_expense(request, id):
    expense = models.Expense.objects.get(id=id)
    expense.paid = True
    expense.save()
    return redirect('expenses')