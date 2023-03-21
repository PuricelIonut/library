from django.urls import path

from . import views


urlpatterns = [ 
    path('', views.home_view, name='home'),
    path('shelf/book/<int:pk>/', views.book_view, name='book'),
    path('shelf/', views.search_books_view, name='search_books'),
    path('shelf/filter/', views.filter_books_view, name='books_filter'),
    path('shelf/filters/', views.filter_all_books, name="test"),

    # Book manager 
    path('shelf/manager/', views.manager_all, name='manager_all'),
    path('shelf/manager/item-edit/<int:pk>', views.manager_item_edit, name='manager_item_edit'),
    path('shelf/manager/item-edit-quick/<int:pk>/', views.manager_quick_edit, name='manager_quick_edit'),
    path('shelf/manager/item-add/', views.manager_item_add, name='manager_item_add'),
    path('shelf/manager/item-remove/<int:pk>', views.manager_item_delete, name='manager_item_delete'),
    path('shelf/manager/item-search/', views.manager_item_search, name='manager_item_search'),
    
    ]