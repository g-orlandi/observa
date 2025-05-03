from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomUserCreationForm

from main import api
from backend.models import Server

@login_required
def dashboard(request, path):
    data = api.get_main_data()
    return render(request, 'frontend/pages/dashboard.html', {
        'data': data
    })

class ListServersView(LoginRequiredMixin, ListView):
    model = Server
    template_name = "frontend/pages/servers.html"

class UpdateServerView(LoginRequiredMixin, UpdateView):
    model = Server
    fields = ['name', 'description', 'url', 'port', 'logo']
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/components/update_server_modal.html"

class DeleteServerView(LoginRequiredMixin, DeleteView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/components/delete_server_confirmation_modal.html"

class CreateServerView(LoginRequiredMixin, CreateView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    fields = ['name', 'description', 'url', 'port', 'logo']
    template_name = "frontend/components/create_server_modal.html"

class UserCreateView(CreateView):
    form_class = CustomUserCreationForm
    template_name = "frontend/users/auth_base.html"
    success_url = reverse_lazy("frontend:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            "page_title": "Registration",
            "header_text": "Create a new account",
            "button_text": "Sign Up",
            "extra_links": '<a href="/login/">Already have an account?</a>'
        })
        return context