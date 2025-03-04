from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.forms import AuthenticationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username","first_name","last_name","email","password1","password2")
        widgets ={
            "username": forms.TextInput(
                attrs={"placeholder": "Enter your username", "class": "form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"placeholder": "Enter your email", "class": "form-control"}

            ),
            "password1": forms.PasswordInput(
                attrs={"placeholder": "Enter your password", "class": "form-control"}
            ),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Confirm your password", "class": "form-control"}
            ),
        }
        help_texts = {
            'username': '',  # Remove the help text for username
            'password1':None,
            'password2':None
        }

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False  

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ["username","first_name","last_name","email"]

class PasswordConfirmationForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label="Password"
    )