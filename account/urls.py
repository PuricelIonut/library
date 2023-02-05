from django.urls import path
from .views import register_view, login_view, logout_view, change_password_view, reset_password_view

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change_password'),
    path('reset-password/', reset_password_view, name='reset_password'),

]