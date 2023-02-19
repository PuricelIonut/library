from django.shortcuts import render
from .models import BookModel


def home_view(request):
    books = BookModel.objects.all()
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books': books, 'genres': genres})

def filter_books_view(request, f):
    books = BookModel.objects.filter(genre=f)
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books':books, 'genres':genres})
