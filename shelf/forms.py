from django import forms
from django.forms import ModelForm
from .models import BookModel


class BookModelForm(ModelForm):
    
    class Meta:
        model = BookModel
        fields ='__all__'
