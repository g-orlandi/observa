import uuid
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'frontend'

urlpatterns = [
    re_path(r'^(dashboard/)?$', views.dashboard, name="dashboard"),
    path('servers/', views.ListServersView.as_view(), name="servers"),
    path('server-info/', views.single_server_info, name="single_server"),
    path('servers/<uuid:pk>/edit/', views.UpdateServerView.as_view(), name="server_edit"),
    path('servers/create/', views.CreateServerView.as_view(), name="server_create"),
    path('servers/<uuid:pk>/delete/', views.DeleteServerView.as_view(), name="server_delete"),
    path('register/', views.UserCreateView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(
        template_name="frontend/users/auth_base.html",
        extra_context={
            "page_title": "Login",
            "header_text": "Sign-in",
            "button_text": "Sign In",
            "extra_links": '<a href="/password-reset/">Forgot your password?</a> <br> <hr> <a href="/register/">Create a new account</a>'
        }
    ), name="login"),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.UserUpdateView.as_view(), name='edit_profile'),
    path('set_active_server/', views.set_active_server, name='set_active_server'),

]