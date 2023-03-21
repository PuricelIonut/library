import django_filters
from .models import BookModel

class BookFilter(django_filters.FilterSet):
    price = django_filters.RangeFilter()

    class Meta:
        model = BookModel
        fields = {
            'genre':['icontains'],
            'language':['icontains'],
            'pages':['exact'],
        }