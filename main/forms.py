from django import forms
from .models import CustomUser, Payment
from django.contrib.auth.forms import UserCreationForm
from .models import Practice




class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class PracticeForm(forms.ModelForm):
    class Meta:
        model = Practice
        fields = ['name', 'description', 'coach', 'date', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

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