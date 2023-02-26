from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views


urlpatterns = [ 
    path('', views.home_view, name='home'),
    path('shelf/book/<int:pk>', views.book_view, name='book'),
    path('shelf/', views.search_books_view, name='search_books'),
    path('shelf/filter/genre/<str:genre>', views.filter_books_view, name='books_filter'),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)