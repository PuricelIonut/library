from .models import BookModel

# Get book data to use in templates
class BookData:
    number_of_pages = ['0-100', '100-200', '200-300', '300-500', '500-700', '700-900', '1000+']
    