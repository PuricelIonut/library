from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home_view, name='home'),
    path('shelf/filter/genre/<str:genre>', views.filter_books_view, name='books_filter'),
    ]