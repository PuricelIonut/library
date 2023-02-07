from django.urls import path 
from .views import register_view, login_view, logout_view, change_password_view
from django.contrib.auth import views as auth_views
from .decorators import user_not_authenticated

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('change-password/', change_password_view, name='change_password'),
    # Reset password
    path('reset-password/', user_not_authenticated(auth_views.PasswordResetView.as_view(template_name='account/templates/reset-password/reset-password.html')) , name='reset_password'),
    path('reset-password-sent/', auth_views.PasswordResetDoneView.as_view(template_name='account/templates/reset-password/reset-password-sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='account/templates/reset-password/reset-password-confirm.html'), name='password_reset_confirm'),
    path('reset-password-complete/', auth_views.PasswordResetCompleteView.as_view(template_name='account/templates/reset-password/reset-password-complete.html'), name='password_reset_complete'),

]