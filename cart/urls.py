from django.urls import path
from . import views

urlpatterns = [
    path('update_item/', views.update_item, name='update_item')
]