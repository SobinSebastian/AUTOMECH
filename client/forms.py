from django import forms
from .models import *
from django.utils import timezone
from datetime import datetime, time
class LoginForm(forms.Form):
    email=forms.EmailField(label="email" ,max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class CustomRegistrationForm(forms.Form):
    firstname = forms.CharField(max_length=30)
    lastname = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirmpassword = forms.CharField(widget=forms.PasswordInput)
    