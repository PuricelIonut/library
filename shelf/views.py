from django.shortcuts import render
from .models import BookModel


def home_view(request):
    books = BookModel.objects.all()
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books': books, 'genres': genres})


def filter_books_view(request, genre):
    books = BookModel.objects.filter(genre=genre)
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books':books, 'genres':genres})
