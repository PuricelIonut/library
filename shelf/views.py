from django.shortcuts import render
from .models import BookModel

def home_view(request):
    books = BookModel.objects.all()
    return render(request, 'home.html', {'books': books})