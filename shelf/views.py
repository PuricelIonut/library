from django.shortcuts import render
from django.db.models import Q
from django.http import Http404

from .models import BookModel
from .helpers import BookData


def home_view(request):
    return render(
        request,
        "home.html",
        {
            "books": BookData.all_books,
            "genres": BookData.genres,
            "languages": BookData.languages,
            "pages": BookData.number_of_pages,
        },
    )


def filter_books_view(request, filter_type, filter_option):
    if filter_type == "genre":
        filtered_results = BookModel.objects.filter(genre=filter_option)
    elif filter_type == "language":
        filtered_results = BookModel.objects.filter(language=filter_option)
    elif filter_type == "pages":
        if "-" in filter_option:
            x = filter_option.split("-")
            filtered_results = BookModel.objects.filter(
                pages__range=[x[0], int(x[1]) + 1]
            )
        elif "+" in filter_option:
            filtered_results = BookModel.objects.filter(pages__range=[300, 9999])

    return render(
        request,
        "home.html",
        {
            "books": filtered_results,
            "genres": BookData.genres,
            "languages": BookData.languages,
            "pages": BookData.number_of_pages,
        },
    )


def search_books_view(request):
    search_term = request.GET.get("search")
    books = BookModel.objects.filter(
        Q(title__icontains=search_term)
        | Q(author__icontains=search_term)
        | Q(genre__icontains=search_term)
        | Q(language__icontains=search_term)
    )
    return render(
        request,
        "home.html",
        {
            "books": books,
            "genres": BookData.genres,
            "languages": BookData.languages,
            "pages": BookData.number_of_pages,
        },
    )


def book_view(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
    return render(request, "book.html", {"book": book})
