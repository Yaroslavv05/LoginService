from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm
from django.contrib.auth import login, get_user_model


def index(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})
