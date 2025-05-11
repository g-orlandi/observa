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

from .forms import EndpointForm
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

################### Dashboard ###################

def _get_up_down_count(query_code, str_entities, count):
    if not str_entities:
        return 0, 0
    try:
        prom_q = PromQuery.objects.get(code=query_code)
        up = int(api.generic_call(str_entities, prom_q, 0))
        down = count - up
        return up, down
    except Exception as e:
        return 0, count
    
@login_required
@require_GET
def get_online_entities(request):
    user = request.user

    servers = user.get_accessible_servers_string()
    servers_up, servers_down = _get_up_down_count("is-on-all", servers, len(user.get_accessible_servers()))

    endpoints = user.get_accessible_endpoints_string()
    endpoints_up, endpoints_down = _get_up_down_count("monitor-status-all", endpoints, len(user.get_accessible_endpoints()))

    return JsonResponse({
        'entities': {
            'up': servers_up + endpoints_up,
            'down': servers_down + endpoints_down,
        },
        'servers': {
            'up': servers_up,
            'down': servers_down,
        },
        'endpoints': {
            'up': endpoints_up,
            'down': endpoints_down,
        },
    })


######################################################

@login_required
@require_GET
def get_entity_status(request):
    qtype = 0
    source = request.GET.get("source", "server")
    if source == "server":
        active_server = request.user.active_server
        parameter = f"{active_server.domain}:{active_server.port}"
        metric = 'is-on'
    elif source == "endpoint":
        active_endpoint = request.user.active_endpoint
        parameter = active_endpoint.url
        metric = 'monitor-status'
    
    prom_query = PromQuery.objects.get(code=metric)

    dim = "22px"
    
    response = api.generic_call(parameter, prom_query, qtype)
    color = "green" if int(response) == 1 else "red"
    html = f'<span style="display:inline-block; width:{dim}; height:{dim}; border-radius:50%; background:{color};margin-top: 5px;"></span>'
    return HttpResponse(html)


######################################################

################### Endpoints list ###################

class ListEndpointsView(LoginRequiredMixin, ListView):
    model = Endpoint
    template_name = "frontend/pages/endpoints.html"

    def get_queryset(self):
        user = self.request.user
        return user.get_accessible_endpoints()

class DeleteEndpointView(LoginRequiredMixin, DeleteView):
    model = Endpoint
    success_url = reverse_lazy('frontend:endpoints')
    template_name = "frontend/components/delete_endpoint_confirmation.html"

    
def edit_endpoint(request, endpoint_id=None):
    import time
    if settings.DEBUG:
        time.sleep(1.0)
    
    if endpoint_id is None:
        endpoint = None
    else:
        endpoint = get_object_or_404(Endpoint, id=endpoint_id)
    
    if request.method == 'POST':
        form = EndpointForm(data=request.POST, instance=endpoint)
        if form.is_valid():
            form.save()
    
    else:
        form = EndpointForm(instance=endpoint)

    return render(request, 'frontend/components/endpoint_form.html', {
        'form': form,
        'action': '',
    })



######################################################

################### Resources ########################

@login_required
@require_GET
def get_instantaneous_data(request, metric):
    prom_query = PromQuery.objects.get(code=metric)

    qtype = 0

    source = request.GET.get("source", "server")
    if source == "server":
        active_server = request.user.active_server
        assert prom_query.target_system == PromQuery.TargetSystem.PROMETHEUS, "Absent metric for Server obj."
        parameter = f"{active_server.domain}:{active_server.port}"
    elif source == "endpoint":
        active_endpoint = request.user.active_endpoint
        assert prom_query.target_system == PromQuery.TargetSystem.UPTIME, "Absent metric for Endpoint obj."
        parameter = active_endpoint.url
    
    try:
        data = api.generic_call(parameter, prom_query, qtype)
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse("None")

@login_required
@require_GET
def get_range_data(request, metric, step=900):
    prom_query = PromQuery.objects.get(code=metric)
    qtype = 1
    user = request.user

    source = request.GET.get("source", "server")
    all = request.GET.get("all", "0")
    all = int(all)
    if source == "server":
        assert prom_query.target_system == PromQuery.TargetSystem.PROMETHEUS, "Absent metric for Server obj."
        if all:
            parameter = user.get_accessible_servers_string()
        else:
            active_entity = request.user.active_server
            parameter = f"{active_entity.domain}:{active_entity.port}"
    elif source == "endpoint":
        assert prom_query.target_system == PromQuery.TargetSystem.UPTIME, "Absent metric for Endpoint obj."
        if all:
            parameter = user.get_accessible_endpoints_string()
        else:
            active_entity = request.user.active_endpoint
            parameter = active_entity.url

    
    date_filter = user.get_active_date_filters()
    range_suffix = api._generate_range_suffix(date_filter['date_from'], date_filter['date_to'], step)

    try:
        data = api.generic_call(parameter, prom_query, qtype, range_suffix)
        labels = [datetime.fromtimestamp(v[0]).isoformat() for v in data]
        values = [float(v[1]) for v in data]
        return JsonResponse({"labels": labels, "values": values, "title": prom_query.title})
    except Exception as e:
        return JsonResponse({"error": "Metric not found"}, status=404)

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

