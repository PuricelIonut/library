from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator

from .forms import BookModelForm
from .models import BookModel
from .filters import BookFilter

# Usefull variables
books = BookModel.objects.all()
number_of_pages = [
    "0-100",
    "100-200",
    "200-300",
    "300-500",
    "500-700",
    "700-900",
    "1000+",
]


def home_view(request):
    p = Paginator(BookModel.objects.filter().order_by("id"), 10)
    page = request.GET.get("page")
    book_pages = p.get_page(page)
    return render(
        request,
        "home.html",
        {
            "books": book_pages,
            "items": book_pages,
            "genres": books.values("genre").distinct(),
            "languages": books.values("language").distinct(),
            "titles": books.values("title").distinct(),
            "authors": books.values("author").distinct(),
            "pages": number_of_pages,
        },
    )


def filter_books_view(request):
    f = BookFilter(request.GET, queryset=BookModel.objects.all())

    p = Paginator(f.qs, 10)
    page = request.GET.get("page")
    book_pages = p.get_page(page)

    return render(
        request,
        "home.html",
        {   'form': f.form,
            "items": book_pages,
            "books": f.qs,
            "genres": books.values("genre").distinct(),
            "languages": books.values("language").distinct(),
            "titles": books.values("title").distinct(),
            "authors": books.values("author").distinct(),
            "pages": number_of_pages,
        },
    )


def search_books_view(request):
    search_term = request.GET.get("search")
    found_books = BookModel.objects.filter(
        Q(title__icontains=search_term)
        | Q(author__icontains=search_term)
        | Q(genre__icontains=search_term)
        | Q(language__icontains=search_term)
    )
    p = Paginator(found_books, 10)
    page = request.GET.get("page")
    book_pages = p.get_page(page)
    return render(
        request,
        "home.html",
        {
            "items": book_pages,
            "books": found_books,
            "genres": books.values("genre").distinct(),
            "languages": books.values("language").distinct(),
            "titles": books.values("title").distinct(),
            "authors": books.values("author").distinct(),
            "pages": number_of_pages,
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
    p = Paginator(BookModel.objects.filter().order_by("id"), 20)
    page = request.GET.get("page")
    books = p.get_page(page)
    search_id = request.GET.get("search")
    if request.user.is_staff or request.user.is_superuser:
        return render(request, "manager.html", {"items": books, "search_id": search_id})
    else:
        return redirect("home")


@login_required
def manager_item_edit(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "POST":
            form = BookModelForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                messages.success(request, "Item succesfully modified!")
                return redirect("manager_all")
            else:
                messages.error(request, "Please fill all the fields correctly!")
        else:
            form = BookModelForm(instance=book)
        return render(request, "manager_item.html", {"book": book, "form": form})
    else:
        return redirect("home")


@login_required
def manager_item_add(request):
    if request.user.is_staff or request.user.is_superuser:
        if request.method == "POST":
            form = BookModelForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Item succesfully added!")
                return redirect("manager_all")
            else:
                messages.error(request, "Please fill all the fields correctly!")
        else:
            form = BookModelForm()
        return render(request, "manager_item.html", {"form": form})
    else:
        return redirect("home")


@login_required
def manager_item_delete(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
    book.delete()
    messages.success(request, "Item succesfully deleted!")
    return redirect("manager_all")


def manager_item_search(request):
    id = request.GET.get("item")
    return manager_item_edit(request, pk=id)


def manager_quick_edit(request, pk):
    obj = BookModel.objects.get(id=pk)
    qty = request.GET.get(str(obj.id))
    prc = request.GET.get(obj.title)
    try:
        if qty and not prc:
            obj.quantity = qty
            obj.save()
            messages.success(
                request,
                mark_safe(
                    f"<b>Quantity</b> succesfully modified for item: <br><b>ID: {obj.id}</b> <br><b>Title: {obj.title}</b>"
                ),
            )
        elif prc and not qty:
            obj.price = prc
            obj.save()
            messages.success(
                request,
                mark_safe(
                    f"<b>Price</b> succesfully modified for item: <br><b>ID: {obj.id}</b> <br><b>Title: {obj.title}</b>"
                ),
            )
        else:
            obj.quantity = qty
            obj.price = prc
            obj.save()
            messages.success(
                request,
                mark_safe(
                    f"<b>Quantity</b> and <b>Price</b> succesfully modified for item: <br><b>ID: {obj.id}</b> <br><b>Title: {obj.title}</b>"
                ),
            )
    except:
        messages.error(
            request, f"There was a problem processing your request.Please try again!"
        )
    return redirect("manager_all")


def test_filters(request):
    f = BookFilter(request.GET, queryset=BookModel.objects.all())
    return render(request, 'test.html', {'books': f.qs, 'form':f.form})