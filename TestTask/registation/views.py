from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserLoginForm
from .models import ProfileModel
from django.contrib.auth import login
from django.contrib.auth.models import User


def index(request):
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            user_id = User.objects.get(username=form.cleaned_data['username']).id
            response = redirect('profile')
            response.set_cookie('user_id', user_id)
            return response
        else:
            messages.error(request, 'Ошибка авторизации')
    else:
        form = UserLoginForm()
    return render(request, 'login.html', {'form': form})


def profile(request):
    username = ProfileModel.objects.get(user_id=request.COOKIES['user_id']).username
    full_name = ProfileModel.objects.get(user_id=request.COOKIES['user_id']).full_name
    photo = ProfileModel.objects.get(user_id=request.COOKIES['user_id']).photo_profile
    return render(request, 'profile.html', {'username': username, 'full_name': full_name, 'photo_profile': photo})
