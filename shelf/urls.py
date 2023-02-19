from django.urls import path
from . import views


urlpatterns = [ 
    path('', views.home_view, name='home'),
    path('shelf/filter/<str:f>', views.filter_books_view, name='filter_books'),
    ]