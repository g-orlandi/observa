import uuid
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'frontend'

urlpatterns = [
    re_path(r'^(dashboard/)?$', views.dashboard, name="dashboard"),
    path('servers/', views.ListServersView.as_view(), name="servers"),
    path('servers/<uuid:pk>/edit/', views.UpdateServerView.as_view(), name="server_edit"),
    path('servers/create/', views.CreateServerView.as_view(), name="server_create"),
    path('servers/<uuid:pk>/delete/', views.DeleteServerView.as_view(), name="server_delete"),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(
        template_name="frontend/users/auth_base.html",
        extra_context={
            "page_title": "Login",
            "header_text": "Sign in to your account",
            "button_text": "Sign In",
            "extra_links": '<a href="/password-reset/">Forgot your password?</a>'
        }
    ), name="login"),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]