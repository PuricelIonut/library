from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUserModel

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUserModel
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class UserInfoForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)