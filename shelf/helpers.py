from .models import BookModel

# Get book data to use in templates
class BookData:
    all_books = BookModel.objects.all()
    titles = BookModel.objects.values('title').distinct()
    authors = BookModel.objects.values('author').distinct()
    genres = BookModel.objects.values('genre').distinct()
    languages = BookModel.objects.values('language').distinct()
    number_of_pages = ['0-100', '100-200', '200-300', '300+']
    