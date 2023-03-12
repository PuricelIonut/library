from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.safestring import mark_safe


from .forms import BookModelForm
from .models import BookModel
from .helpers import BookData


def home_view(request):
    books = BookModel.objects.all()
    return render(
        request,
        "home.html",
        {
            "books": books,
            "genres": books.values('genre').distinct(),
            "languages": books.values('language').distinct(),            
            "titles": books.values('title').distinct(),
            "authors": books.values('author').distinct(),
            "pages": BookData.number_of_pages,
        },
    )


def filter_books_view(request, filter_type, filter_option):
    books = BookModel.objects.all()
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
            "genres": books.values('genre').distinct(),
            "languages": books.values('language').distinct(),            
            "titles": books.values('title').distinct(),
            "authors": books.values('author').distinct(),
            "pages": BookData.number_of_pages,
            "fil_option": filter_option,
            "fil_type": filter_type,
        },
    )


def search_books_view(request):
    all_books = BookModel.objects.all()
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
            "genres": books.values('genre').distinct(),
            "languages": books.values('language').distinct(),            
            "titles": books.values('title').distinct(),
            "authors": books.values('author').distinct(),
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
    books = BookModel.objects.all().order_by('id')
    search_id = request.GET.get('search')
    if request.user.is_staff or request.user.is_superuser:
        return render(request, 'manager.html', {'books': books, 'search_id': search_id})
    else:
        return redirect('home')
    

@login_required
def manager_item_edit(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
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
    

@login_required
def manager_item_delete(request, pk):
    try:
        book = BookModel.objects.get(id=pk)
    except:
        raise Http404()
    book.delete()
    messages.success(request, 'Item succesfully deleted!')
    return redirect('manager_all')


def manager_item_search(request):
    id = request.GET.get('item')
    return manager_item_edit(request, pk=id)


def manager_quick_edit(request, pk):
    obj = BookModel.objects.get(id=pk)
    qty = request.GET.get(str(obj.id))
    prc = request.GET.get(obj.title)
    try:
        if qty and not prc:
            obj.quantity = qty
            obj.save()
            messages.success(request, mark_safe(f"<b>Quantity</b> succesfully modified for item: <br><b>ID: {obj.id}</b> <br><b>Title: {obj.title}</b>"))
        elif prc and not qty:
            obj.price = prc
            obj.save()
            messages.success(request, mark_safe(f"<b>Price</b> succesfully modified for item: <br><b>ID: {obj.id}</b> <br><b>Title: {obj.title}</b>"))
        else:
            obj.quantity = qty
            obj.price = prc
            obj.save()
            messages.success(request, mark_safe(f"<b>Quantity</b> and <b>Price</b> succesfully modified for item: <br><b>ID: {obj.id}</b> <br><b>Title: {obj.title}</b>"))  
    except:
        messages.error(request, f"There was a problem processing your request.Please try again!")
    return redirect('manager_all')