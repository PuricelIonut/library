from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views
from .decorators import user_not_authenticated

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
    #path('reset-password/', password_reset_view, name='password_reset'),
]