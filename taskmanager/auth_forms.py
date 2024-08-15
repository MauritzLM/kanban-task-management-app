from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User

class SignUpForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)   