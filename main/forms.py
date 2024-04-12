from django import forms
from .models import CustomUser, Payment
from django.contrib.auth.forms import UserCreationForm
from .models import Practice




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
        self.fields['member'].label_from_instance = lambda obj: obj.first_name

    class Meta:
        model = CustomUser
        fields = ['member']  

class CreatePracticeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        coach_group = CustomUser.objects.filter(groups__name='Coach')
        self.fields['coach'].queryset = coach_group
        self.fields['coach'].label_from_instance = lambda obj: obj.first_name

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
            self.fields['members'].label_from_instance = lambda obj: obj.first_name

    class Meta:
        model = Practice
        fields = ['members']

class ManagePracticeCoachesForm(forms.ModelForm):
    practice = forms.ModelChoiceField(queryset=Practice.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['coach'].queryset = CustomUser.objects.filter(groups__name='Coach')
        self.fields['coach'].label_from_instance = lambda obj: obj.first_name

    class Meta:
        model = Practice
        fields = ['practice', 'coach']

class PaymentForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['practice'].queryset = Practice.objects.exclude(payment__user=self.user)
        self.fields['practice'].label_from_instance = lambda obj: obj.name

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