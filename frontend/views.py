from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404

from main import api
from backend.models import Server

@login_required
def dashboard(request, path):
    active_server = request.user.active_server
    data = api.get_main_data(active_server)
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
    
class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    template_name = "frontend/users/edit.html"
    success_url = reverse_lazy('frontend:dashboard')
    fields = ['username', 'email', 'profile_picture']

    def get_object(self):
        return self.request.user
    
@login_required
@require_POST
def set_active_server(request):
    server_id = request.POST.get('server_id')
    if server_id:
        server = get_object_or_404(Server, id=server_id, user=request.user)
        request.user.active_server = server
        request.user.save()
    return redirect(request.META.get('HTTP_REFERER', 'frontend:dashboard'))