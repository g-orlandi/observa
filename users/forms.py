from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

# Register your models here.

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email")  # aggiungi i campi che usi

    def save(self, commit=True):
        user = super().save(commit)
        base_group = Group.objects.get(name="Base")
        user.groups.add(base_group)
        return user