import uuid
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(
        template_name="users/auth_base.html",
        extra_context={
            "page_title": "Login",
            "header_text": "Sign-in",
            "button_text": "Sign In",
            "extra_links": '<a href="/password-reset/">Forgot your password?</a> <br> <hr> <a href="/register/">Create a new account</a>'
        }
    ), name="login"),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.UserUpdateView.as_view(), name='edit_profile'),
]