from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.NumberInput()

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'password1', 'password2']
