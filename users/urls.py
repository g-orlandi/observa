import uuid
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.UserCreateView.as_view(), name='register'),
    path("login/", auth_views.LoginView.as_view(
        template_name="users/base.html",
        extra_context={
            "page_title": "Login",
            "header_text": "Sign-in",
            "button_text": "Sign In",
            "extra_links": '<a href="/password-reset/">Forgot your password?</a> <br> <hr> <a href="/register/">Create a new account</a>'
        }
    ), name="login"),    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('edit_profile/', views.UserUpdateView.as_view(), name='edit_profile'),

    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path(
        'password-reset-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            success_url=reverse_lazy('users:password_reset_complete')  # ← qui la modifica
        ),
        name='password_reset_confirm'
    ),
    path('password-reset-complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
        name='password_reset_complete'),

    path('set-active-server/', views.set_active_server, name='set_active_server'),
    path('set-active-endpoint/', views.set_active_endpoint, name='set_active_endpoint'),
    path('set-date-range/', views.set_date_range, name='set_date_range'),

]