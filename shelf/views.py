from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import BookModelForm
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
            "titles":BookData.titles,
            "authors":BookData.authors,
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
            filtered_results = BookModel.objects.filter(pages__range=[1000, 9999])

    return render(
        request,
        "home.html",
        {
            "books": filtered_results,
            "genres": BookData.genres,
            "languages": BookData.languages,
            "titles":BookData.titles,
            "authors":BookData.authors,
            "pages": BookData.number_of_pages,
            "fil_option": filter_option,
            "fil_type": filter_type,
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
            "titles":BookData.titles,
            "authors":BookData.authors,
            "pages": BookData.number_of_pages,
        },
    )


def book_view(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
    return render(request, "book.html", {"book": book})


@login_required
def manager_all(request):
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'manager.html', {'books': BookData.all_books})
    else:
        return redirect('home')
    

@login_required
def manager_item_edit(request, pk):
    book = BookModel.objects.get(id=pk)
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = BookModelForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                messages.success(
                request, "Item succesfully modified!")
                return redirect('manager_all')
            else:
                messages.error(request, "Please fill all the fields correctly!")
        else:
            form = BookModelForm(instance=book)
        return render(request, 'manager_item.html', {'book': book, 'form': form})
    else:
        return redirect('home')


@login_required
def manager_item_add(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == 'POST':
            form = BookModelForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                request, "Item succesfully added!")
                return redirect('manager_all')
            else:
                messages.error(request, "Please fill all the fields correctly!")
        else:
            form = BookModelForm()
        return render(request, 'manager_item.html', {'form': form})
    else:
        return redirect('home')