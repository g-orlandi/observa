from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy

from backend.models import Server

# Create your views here.
def dashboard(request, path):
    return render(request, 'frontend/index.html', {
        'path':path
    })

def hello_world(request):
    assert request.htmx, "Not authorized request!"
    return render(request, 'frontend/hello_world.html', {
    })

class ListServersView(ListView):
    model = Server
    template_name = "frontend/servers.html"

class UpdateServerView(UpdateView):
    model = Server
    fields = ['name', 'description']
    success_url = reverse_lazy('frontend:servers')

class DeleteServerView(DeleteView):
    model = Server
    success_url = reverse_lazy('frontend:servers')