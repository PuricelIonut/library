from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUserModel

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUserModel
        fields = ('username', 'email', 'password1', 'password2')
