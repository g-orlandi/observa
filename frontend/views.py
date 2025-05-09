from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.forms import CustomUserCreationForm
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST, require_GET
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import timedelta, datetime
from main import api
from django.http import JsonResponse, HttpResponseBadRequest


from backend.models import Server, PromQuery, Endpoint
import requests
from main import settings
from requests.auth import HTTPBasicAuth
import re

################### Main pages ###################

@login_required
@require_GET
def dashboard(request, path):
    return render(request, 'frontend/pages/dashboard.html', {
    })

@login_required
@require_GET
def resources(request):
    return render(request, 'frontend/pages/resources.html', {
    })

@login_required
@require_GET
def network(request):
    return render(request, 'frontend/pages/network.html', {
    })

@login_required
@require_GET
def report(request):
    return render(request, 'frontend/pages/report.html', {
    })

@login_required
@require_GET
def backup(request):
    return render(request, 'frontend/pages/backup.html', {
    })

################### Servers list ###################

class ListServersView(LoginRequiredMixin, ListView):
    model = Server
    template_name = "frontend/pages/servers.html"

class UpdateServerView(LoginRequiredMixin, UpdateView):
    model = Server
    fields = ['name', 'description', 'domain', 'port', 'logo']
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/modals/update_server_modal.html"

class DeleteServerView(LoginRequiredMixin, DeleteView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/modals/delete_server_confirmation_modal.html"

class CreateServerView(LoginRequiredMixin, CreateView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    fields = ['name', 'description', 'domain', 'port', 'logo', 'group']
    template_name = "frontend/modals/create_server_modal.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

@login_required
@require_GET
def get_entity_status(request):

    source = request.GET.get("source", "server")
    if source == "server":
        active_entity = request.user.active_server
        metric = 'is-on'
    elif source == "endpoint":
        active_entity = request.user.active_endpoint
        metric = 'monitor-status'

    dim = "22px"
    
    response = api.get_instantaneous_data(active_entity, metric)
    color = "green" if int(response) == 1 else "red"
    html = f'<span style="display:inline-block; width:{dim}; height:{dim}; border-radius:50%; background:{color};margin-top: 5px;"></span>'
    return HttpResponse(html)


######################################################

################### Endpoints list ###################

class ListEndpointsView(LoginRequiredMixin, ListView):
    model = Endpoint
    template_name = "frontend/pages/endpoints.html"

class CreateEndpointView(LoginRequiredMixin, CreateView):
    model = Endpoint
    success_url = reverse_lazy('frontend:endpoints')
    fields = ['name', 'description', 'url', 'check_keyword', 'logo', 'group']
    template_name = "frontend/modals/create_endpoint_modal.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class UpdateEndpointView(LoginRequiredMixin, UpdateView):
    model = Endpoint
    fields = ['name', 'description', 'url', 'check_keyword', 'logo']
    success_url = reverse_lazy('frontend:endpoints')
    template_name = "frontend/modals/update_endpoint_modal.html"

class DeleteEndpointView(LoginRequiredMixin, DeleteView):
    model = Endpoint
    success_url = reverse_lazy('frontend:endpoints')
    template_name = "frontend/components/delete_endpoint_confirmation_modal.html"

######################################################

################### Resources ########################

@login_required
@require_GET
def get_instantaneous_data(request, metric):
    source = request.GET.get("source", "server")
    if source == "server":
        active_entity = request.user.active_server
    elif source == "endpoint":
        active_entity = request.user.active_endpoint
    
    try:
        data = api.get_instantaneous_data(active_entity, metric)
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse("None")

@login_required
@require_GET
def get_range_data(request, metric):
    user = request.user
    source = request.GET.get("source", "server")
    if source == "server":
        active_entity = request.user.active_server
    elif source == "endpoint":
        active_entity = request.user.active_endpoint

    date_filter = user.get_active_date_filters()
    start_date = date_filter['date_from']
    end_date = date_filter['date_to']

    try:
        data = api.get_range_data(active_entity, metric, start_date, end_date)
    except Exception as e:
        return JsonResponse({"error": "Metric not found"}, status=404)

    return JsonResponse(data)

@login_required
@require_POST
def set_active_server(request):
    server_id = request.POST.get('server_id')
    if server_id:
        request.user.active_server_id = server_id
        request.user.save()
    return redirect(request.META.get('HTTP_REFERER', 'frontend:dashboard'))

@login_required
@require_POST
def set_active_endpoint(request):
    endpoint_id = request.POST.get('endpoint_id')
    if endpoint_id:
        request.user.active_endpoint_id = endpoint_id
        request.user.save()
    return redirect(request.META.get('HTTP_REFERER', 'frontend:dashboard'))


@login_required
@require_POST
def set_date_range(request):
    user = request.user
    try:
        user.set_active_date_filters(request.POST['start_date'], request.POST['end_date'])
        return HttpResponse(status=204)
    except Exception as e:
        return HttpResponseBadRequest(e)

######################################################

def my_box(request):
    query = request.GET.get('query', 'unknown')
    import time, random
    n = random.randint(0,3)
    time.sleep(n)
    return HttpResponse(query)