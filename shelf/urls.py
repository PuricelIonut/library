from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.home_view, name='home'),
    path('shelf/book/<int:pk>/', views.book_view, name='book'),
    path('shelf/', views.search_books_view, name='search_books'),
    path('shelf/filter/<str:filter_type>/<str:filter_option>/', views.filter_books_view, name='books_filter'),
    
    # Book manager 
    path('shelf/manager/', views.manager_all, name='manager_all'),
    path('shelf/manager/item/<int:pk>', views.manager_item_edit, name='manager_item_edit'),
    path('shelf/manager/item-add/', views.manager_item_add, name='manager_item_add'),
    ]