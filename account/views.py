from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'User created succesfully!')
            return redirect('home')
        messages.error(request, 'Invalid credentials')
    form = UserRegisterForm()
    return render(request, 'register.html', context={'register_form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username = username, password = password)
            if user is not None:
                login(request, user)
                messages.info(request, f'You are now logged in as {username}')
                return redirect('home')
            else:
                messages.error(request, f'Invalid username or password')
    form = AuthenticationForm()
    return render(request, 'login.html', context={'login_form': form})


def logout_view(request):
    logout(request)
    return redirect('home')