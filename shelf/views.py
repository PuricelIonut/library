from django.shortcuts import render
from django.db.models import Q
from django.http import Http404

from .models import BookModel


def home_view(request):
    books = BookModel.objects.all()
    genres = BookModel.objects.values('genre').distinct()
    languages = BookModel.objects.values('language').distinct()
    return render(request, 'home.html', {'books': books, 'genres': genres, 'languages':languages})


def filter_books_view(request, filter_type, filter_option):
    genres = BookModel.objects.values('genre').distinct()
    languages = BookModel.objects.values('language').distinct()
    if filter_type == 'genre':
        filtered_results  = BookModel.objects.filter(genre=filter_option)
    elif filter_type == 'language':
        filtered_results  = BookModel.objects.filter(language=filter_option)
    elif filter_type == 'pages':
        if '-' in filter_option:
            temp = filter_option.split('-')
            x = range(int(temp[0]), int(temp[1]) + 1)
        elif '+' in filter_option:
            x = range(300, 9999)
        filtered_results = BookModel.objects.filter(pages__range=x)

    return render(request, 'home.html', {'books':filtered_results, 'genres':genres, 'languages':languages})


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