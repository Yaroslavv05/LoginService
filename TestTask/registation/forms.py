from django.contrib.auth.forms import AuthenticationForm
from django import forms


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Ім'я користувача:", widget=forms.TextInput(attrs={"class": 'form-control'}))
    password = forms.CharField(label="Пароль:", widget=forms.PasswordInput(attrs={"class": 'form-control'}))