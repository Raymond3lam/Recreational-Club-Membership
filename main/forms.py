from django import forms
from django.utils.html import format_html
from .models import CustomUser, Payment, Announcement, Practice
from django.contrib.auth.forms import UserCreationForm

class AnnouncementForm(forms.ModelForm):
    group = forms.ChoiceField(
        choices=[('all', 'All Members'), ('coaches', 'Coaches'), ('members', 'Members')], 
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
        self.fields['target'].queryset = CustomUser.objects.exclude(id=self.user.id)
        self.fields['target'].label_from_instance = self.label_from_instance

    def label_from_instance(self, obj):
        if obj.groups.filter(name='Coach').exists():
            group = 'coaches'
        elif obj.groups.filter(name='Member').exists():
            group = 'members'
        else:
            group = ''
        return format_html('<label data-group="{}">{}</label>', group, obj.get_full_name())

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
        choices=[('all', 'All Members'), ('coaches', 'Coaches'), ('members', 'Members')], 
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
        if obj.groups.filter(name='Coach').exists():
            group = 'coaches'
        elif obj.groups.filter(name='Member').exists():
            group = 'members'
        else:
            group = ''
        return format_html('<label data-group="{}">{}</label>', group, obj.get_full_name())
    
    class Meta:
        model = Announcement
        fields = ['title', 'content', 'group', 'target', 'target_practices']

class RegisterForm(UserCreationForm):
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
        self.fields['member'].queryset = member_group
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
            self.fields['members'].queryset = CustomUser.objects.filter(groups__name='Member').exclude(member_practices=self.instance)
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
        self.fields['practice'].queryset = Practice.objects.exclude(members=self.user)
        self.fields['practice'].label_from_instance = lambda obj: f"{obj.name} - {obj.coach.first_name} {obj.coach.last_name}"

    payment_method = forms.ChoiceField(choices=[('credit', 'Credit Card'), ('debit', 'Debit Card')])
    card_number = forms.CharField()
    expiration_date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m', attrs={'type': 'month'}),
        input_formats=('%Y-%m', )
    )
    cvv = forms.CharField()
    
    class Meta:
        model = Payment
        fields = ['payment_method', 'card_number', 'expiration_date', 'cvv', 'practice']

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user
        instance.amount = 10
        if commit:
            instance.save()
        return instance