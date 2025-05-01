from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy

from backend.models import Server

# Create your views here.
def dashboard(request, path):
    return render(request, 'frontend/pages/dashboard.html', {
        'path':path
    })

def hello_world(request):
    assert request.htmx, "Not authorized request!"
    return render(request, 'frontend/hello_world.html', {
    })

class ListServersView(ListView):
    model = Server
    template_name = "frontend/pages/servers.html"

class UpdateServerView(UpdateView):
    model = Server
    fields = '__all__'
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/components/update_server_modal.html"

class DeleteServerView(DeleteView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/components/delete_server_confirmation_modal.html"

class CreateServerView(CreateView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    fields= '__all__'
    template_name = "frontend/components/create_server_modal.html"
