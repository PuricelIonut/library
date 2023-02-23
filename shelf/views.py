from django.shortcuts import render
from django.db.models import Q
from django.http import Http404

from .models import BookModel


def home_view(request):
    books = BookModel.objects.all()
    genres = BookModel.objects.values('genre').distinct()
    languages = BookModel.objects.values('language').distinct()
    return render(request, 'home.html', {'books': books, 'genres': genres, 'languages':languages})


def filter_books_view(request, genre):
    books = BookModel.objects.filter(genre=genre)
    genres = BookModel.objects.values('genre').distinct()
    languages = BookModel.objects.values('language').distinct()
    return render(request, 'home.html', {'books':books, 'genres':genres, 'languages':languages})


def search_books_view(request):
    search_term = request.GET.get('search')
    books = BookModel.objects.filter(
        Q(title__icontains=search_term) |
        Q(author__icontains=search_term) |
        Q(genre__icontains=search_term) |
        Q(language__icontains=search_term)
    )
    genres = BookModel.objects.values('genre').distinct()
    languages = BookModel.objects.values('language').distinct()
    return render(request, 'home.html', {'books':books, 'genres': genres, 'languages':languages})


def book_view(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
    return render(request, 'book.html', {'book':book})