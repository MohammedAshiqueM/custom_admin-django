from django import forms
from django.contrib.auth.models import User
# Create your models here.

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'User Name'}),
            'email': forms.TextInput(attrs={'placeholder': 'Email'}),
        }