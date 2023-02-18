from django.shortcuts import render
from .models import BookModel

def home_view(request):
    filter = request.GET.get('filter') if request.GET.get('filter') != None else ''
    books = BookModel.objects.filter(genre__icontains=filter)
    genres = BookModel.objects.values('genre').distinct()
    return render(request, 'home.html', {'books': books, 'genres': genres})
