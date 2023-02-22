from django.shortcuts import render
from django.db.models import Q

from .models import BookModel


def home_view(request):
    books = BookModel.objects.all()
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books': books, 'genres': genres})


def filter_books_view(request, genre):
    books = BookModel.objects.filter(genre=genre)
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books':books, 'genres':genres})


def search_books_view(request):
    search_term = request.GET.get('search')
    books = BookModel.objects.filter(
        Q(title__icontains=search_term) |
        Q(author__icontains=search_term) |
        Q(genre__icontains=search_term) |
        Q(language__icontains=search_term)
    )
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books':books, 'genres': genres})