from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUserModel

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(label='Enter your email address:', required=True)
