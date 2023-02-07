from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm
from .decorators import user_not_authenticated


@user_not_authenticated
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.clean()
            user = form.save()
            login(request, user)
            messages.success(request, 'User created succesfully!')
            return redirect('home')
        messages.error(request, 'Invalid credentials')
    form = UserRegisterForm()
    return render(request, 'register.html', context={'register_form': form})


@user_not_authenticated
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are logged in as { request.user.first_name }')
                return redirect('home')
        else:
            messages.error(request, f'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'login.html', context={'login_form': form})


@login_required
def change_password_view(request):
    user = request.user
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Password changed succesfully! Please login again.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid password')
    form = PasswordChangeForm(user)
    return render(request, 'change-password.html', context={'change_password':form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def not_found_view(request, exception):
    return render(request, 'templates/404.html')
