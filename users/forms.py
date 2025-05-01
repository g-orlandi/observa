from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
# Register your models here.

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")  # aggiungi i campi che usi