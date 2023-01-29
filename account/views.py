from django.shortcuts import render, redirect


def register_view(request):
    context = {}
    return render(request, 'register.html', context)

def login_view(request):
    context = {}
    return render(request, 'login.html', context)

def logout_view(request):
    return redirect('home')