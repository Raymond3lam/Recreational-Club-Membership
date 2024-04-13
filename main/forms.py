from django.db.models import Count
from datetime import date, timedelta
from django import forms
from django.db.models import Sum
from django.utils.html import format_html
from .models import CustomUser, Expense, Payment, Announcement, Practice
from django.contrib.auth.forms import UserCreationForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Div

class AnnouncementForm(forms.ModelForm):
    group = forms.ChoiceField(
        choices=[('all', 'All Members'), ('coaches', 'Coaches'), ('members', 'Members'), ('snakes', 'Snakes')],
    )
    
    target = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'user-checkbox'})
    )

    target_practices = forms.ModelMultipleChoiceField(
        queryset=Practice.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'practice-checkbox'})
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['target'].queryset = CustomUser.objects.exclude(id=self.user.id).exclude(is_superuser=True)
        self.fields['target'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        skip = False
        if obj.groups.filter(name='Coach').exists():
            group = 'coaches'
        elif obj.groups.filter(name='Member').exists():
            group = 'members'
        else:
            group = ''
        if obj.payment_count() < obj.practice_count():
            skip = True
        return format_html('<label data-skip="{}" data-group="{}">{}</label>', skip, group, obj.get_full_name())

    class Meta:
        model = Announcement
        fields = ['title', 'content', 'group', 'target', 'target_practices']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.author = self.user
        if commit:
            instance.save()
            self.save_m2m()
        return instance
    
class UpdateAnnouncementForm(forms.ModelForm):
    group = forms.ChoiceField(
        choices=[('all', 'All Members'), ('coaches', 'Coaches'), ('members', 'Members'), ('snakes', 'Snakes')],
    )
    
    target = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(), 
        required=False, 
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'user-checkbox'})
    )

    target_practices = forms.ModelMultipleChoiceField(
        queryset=Practice.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'practice-checkbox'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['target'].queryset = CustomUser.objects.exclude(id=self.instance.author.id)
        self.fields['target'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        skip = False
        if obj.groups.filter(name='Coach').exists():
            group = 'coaches'
        elif obj.groups.filter(name='Member').exists():
            group = 'members'
        else:
            group = ''
        if obj.payment_count() < obj.practice_count():
            skip = True
        return format_html('<label data-skip="{}" data-group="{}">{}</label>', skip, group, obj.get_full_name())

    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'group', 'target', 'target_practices']

class RegisterForm(UserCreationForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'rows': 3}))
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'phone_number', 'address']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class AddCoachForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=None)

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        member_group = CustomUser.objects.filter(groups__name='Member')
        self.fields['member'].queryset = member_group.exclude(first_name="")
        self.fields['member'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = CustomUser
        fields = ['member']  

class CreatePracticeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coach_group = CustomUser.objects.filter(groups__name='Coach')
        self.fields['coach'].queryset = coach_group
        self.fields['coach'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Practice
        fields = ['name', 'description', 'coach', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class AddMemberToPracticeForm(forms.ModelForm):
    members = forms.ModelChoiceField(queryset=CustomUser.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.id:
            self.fields['members'].queryset = CustomUser.objects.filter(groups__name='Member').exclude(member_practices=self.instance).exclude(is_superuser=True)
            self.fields['members'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Practice
        fields = ['members']

class ManagePracticeCoachesForm(forms.ModelForm):
    coach = forms.ModelChoiceField(queryset=CustomUser.objects.filter(groups__name='Coach'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coach'].label_from_instance = lambda obj: f"{obj.first_name} {obj.last_name}"

    class Meta:
        model = Practice
        fields = ['coach']

class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        paid_practices_ids = self.user.payment_set.values_list('practice', flat=True)
        self.fields['practice'].queryset = Practice.objects.exclude(id__in=paid_practices_ids)
        self.fields['practice'].label_from_instance = lambda obj: f"{obj.name} - {obj.coach.first_name} {obj.coach.last_name}"

    payment_method = forms.ChoiceField(choices=[('credit', 'Credit Card'), ('debit', 'Debit Card')])
    card_number = forms.CharField()
    expiration_date = forms.CharField(label='Expiry Date', max_length=5, help_text='Format: MM/YY')
    cvv = forms.CharField()
    
    class Meta:
        model = Payment
        fields = ['payment_method', 'card_number', 'expiration_date', 'cvv', 'practice']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        amount = 10
        # discount if top ten most attended users
        top_ten = CustomUser.objects.filter(groups__name='Member').exclude(is_superuser=True).annotate(practice_count=Sum('member_practices')).order_by('-practice_count')[:10]
        if instance.user in top_ten:
            amount = amount - amount*0.1
        # check all classes attended within last 3 months 
        three_months_ago = date.today() - timedelta(days=90)
        practices = Practice.objects.filter(date__gte=three_months_ago)
        good_three = True
        for practice in practices:
            if not practice.paid(instance.user):
                good_three = False
                break
        if good_three:
            amount = amount - amount*0.1
        else:
            amount = amount + amount*0.2
        instance.amount = amount
        if commit:
            instance.save()
            practice = instance.practice
            practice.members.add(self.user)
            practice.save()
        return instance

class ExpenseForm(forms.ModelForm):
    category = forms.ChoiceField(choices=[('Hall', 'Hall'), ('Other', 'Other')])
    class Meta:
        model = Expense
        fields = ['amount', 'due', 'notes', 'category']
        widgets = {
            'due': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }        