from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from users.forms import CustomUserCreationForm

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "users/auth_base.html"
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
    success_url = reverse_lazy('frontend:dashboard')
    fields = ['username', 'email', 'profile_picture']

    def get_object(self):
        return self.request.user
