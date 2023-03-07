from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.home_view, name='home'),
    path('shelf/book/<int:pk>/', views.book_view, name='book'),
    path('shelf/', views.search_books_view, name='search_books'),
    path('shelf/filter/<str:filter_type>/<str:filter_option>/', views.filter_books_view, name='books_filter'),
    
    # Book manager 
    path('shelf/manager/', views.books_manager_all, name='books_manager_all'),
    path('shelf/manager/item/<int:pk>', views.books_manager_item, name='books_manager_item'),

    ]