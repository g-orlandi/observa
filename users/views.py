from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from users.forms import CustomUserCreationForm
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/base.html"
    success_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "page_title": "Registration",
            "header_text": "Create a new account",
            "button_text": "Sign Up",
            "extra_links": '<a href="/login/">Already have an account?</a>'
        })
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "users/edit.html"
    success_url = reverse_lazy('users:edit_profile')
    fields = ['username', 'email', 'profile_picture']

    def get_object(self):
        return self.request.user

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('frontend:dashboard')