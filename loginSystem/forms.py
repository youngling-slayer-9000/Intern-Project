from django import forms
from .models import EmployeeUser
from django.contrib.auth.hashers import make_password, check_password




class EmployeeLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
