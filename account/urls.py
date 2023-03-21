from django.urls import path 
from . import views


urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('change-password/', views.change_password_view, name='change_password'),
    path('reset-password/', views.password_reset_view, name='password_reset'),
    path('reset/<uidb64>/<token>', views.password_reset_confirm ,name='password_reset_confirm'),
    path('user-profile/', views.account_management_view, name='user_panel')
]