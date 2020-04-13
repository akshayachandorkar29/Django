"""
This is the file containing django inbuilt  model forms
Author: Akshaya Revaskar
Date: 02/04/2020
"""
from django.forms import ModelForm
from django.contrib.auth.models import User


class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class ForgotPasswordForm(ModelForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class ResetForm(ModelForm):
    class Meta:
        model = User
        fields = ('password',)