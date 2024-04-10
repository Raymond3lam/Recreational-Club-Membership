from django import forms
from .models import CustomUser
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
        fields = ['name', 'description', 'coach', 'members']
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }