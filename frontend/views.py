from datetime import datetime
from uuid import UUID

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import (
    HttpResponse, JsonResponse, HttpResponseBadRequest, HttpResponseForbidden, HttpResponseRedirect
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET, require_POST
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView

from backend.models import PromQuery, Endpoint, Server
from .forms import EndpointForm
from .decorators import require_pro_user
from main import api, settings
from django.template.loader import render_to_string


################### Main pages ###################

"""
Views used to implement two different entry point, one for PRO user and one for FREE user
"""
@login_required
@require_GET
def index(request):
    if request.user.is_pro:
        return HttpResponseRedirect('/dashboard/')
    return HttpResponseRedirect('/network/')


"""
The synoptic look on all the entity status; it's the entry point for PRO user
"""
@login_required
@require_GET
@require_pro_user
def dashboard(request):
    return render(request, 'frontend/pages/dashboard.html', {
        "graph_include": "frontend/components/graphs.html"
    })

"""
This is the presentation of the metrics for a single SERVER at a time;
PRO user here can have a fine-grained look on their server status.
"""
@login_required
@require_GET
@require_pro_user
def resources(request):
    widgets = [
        {"title": "Operative System", "metric": "os", "url_name": "frontend:get_instantaneous_data", "icon": "bi-gear-fill"},
        {"title": "Server Status", "metric": "", "url_name": "frontend:get_entity_status", "icon": "bi-circle-half"},
        {"title": "Uptime since last boot", "metric": "uptime-days", "url_name": "frontend:get_instantaneous_data", "icon": "bi-clock-history", "unit": "days"},
        {"title": "Http request (5m)", "metric": "http-req", "url_name": "frontend:get_instantaneous_data", "icon": "bi-activity"},
        {"title": "CPU Usage", "metric": "cpu-usage", "url_name": "frontend:get_instantaneous_data", "icon": "bi-cpu", "unit": "%", "col": 3},
        # {"title": "Memory Used", "metric": "mem-used", "url_name": "frontend:get_instantaneous_data", "icon": "bi-memory", "unit": "GB","col": 3},
        # {"title": "Disk Used", "metric": "disk-used", "url_name": "frontend:get_instantaneous_data", "icon": "bi-hdd-fill", "unit": "GB","col": 3},
    ]
    charts = [
        {"id": "cpuChart", "title": "CPU Usage Trend", "metric": "cpu-usage", "color": "#0d6efd"},
        {"id": "memoryChart", "title": "Memory Usage Trend", "metric": "mem-used", "color": "#6610f2"},
        {"id": "diskChart", "title": "Disk Trend", "metric": "disk-used", "color": "#a110a2"},
        {"id": "requestChart", "title": "Http request Trend", "metric": "http-req", "color": "#c110a2"},
    ]
    return render(request, "frontend/pages/resources.html", {
        "widgets": widgets,
        "charts": charts,
    })


"""
This is the presentation of the metrics for a single ENDPOINT at a time;
all user here can have a fine-grained look on their endpoint status.
"""
@login_required
@require_GET
def network(request):
    widgets = [
        {"title": "Endpoint Status", "metric": "", "url_name": "frontend:get_entity_status", "icon": "bi-circle-half", "source": "endpoint"},
        {"title": "Latency", "metric": "response-time", "url_name": "frontend:get_instantaneous_data", "icon": "bi-activity", "source": "endpoint", "unit": "ms"},
        {"title": "Days until cert. expiration", "metric": "cert-days-rem", "url_name": "frontend:get_instantaneous_data", "icon": "bi-lock-fill", "source": "endpoint"},
        {"title": "Uptime (last 30d)", "metric": "uptime-perc", "url_name": "frontend:get_instantaneous_data", "icon": "bi-clock-history", "source": "endpoint", "unit": "%"},
    ]

    charts = [
        {"id": "latencyChart", "title": "Latency trend", "metric": "response-time", "color": "#0d6efd", "col": 12},
        {"id": "uptimeChart", "title": "Uptime trend", "metric": "monitor-status", "color": "#6610f2", "col": 12, "entity": "endpoint"},
    ]

    return render(request, "frontend/pages/info.html", {
        "widgets": widgets,
        "charts": charts,
    })

"""
This is the presentation of the metrics for a single backup-server at a time;
PRO user here can have a fine-grained look on their backup-server status.
"""
@login_required
@require_GET
@require_pro_user
def backup(request):
    widgets = [
        {"title": "Backup status", "metric": "", "url_name": "frontend:get_entity_status", "icon": "bi-circle-half", "source": "backup"},
        {"title": "Last snapshot", "metric": "last-snap-timestamp", "url_name": "frontend:get_instantaneous_data", "icon": "bi-clock-history", "source": "backup", "unit": "hours ago"},
        {"title": "Snapshots count", "metric": "snaps-count", "url_name": "frontend:get_instantaneous_data", "icon": "bi-123", "source": "backup"},
    ]
    charts = [
        {"id": "snapcountChart", "title": "Snapshot count Trend", "metric": "snaps-count", "color": "#a110a2", "col": 12},
        {"id": "filesizeChart", "title": "File size per snapshot Trend", "metric": "snap-file-size", "color": "#6610f2", "col": 12},
        {"id": "filecountChart", "title": "File count per snapshot trend", "metric": "snap-file-count", "color": "#0d6efd", "col": 12},
    ]
    return render(request, "frontend/pages/info.html", {
        "widgets": widgets,
        "charts": charts,
    })


@login_required
@require_GET
@require_pro_user
def report(request):
    return render(request, 'frontend/pages/report.html', {
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


###################################################

@login_required
@require_GET
def get_entity_status(request, entity_id=None):
    qtype = 0
    source = request.GET.get("source", "server")
    
    try:
        if source in ("server", "backup"):
            if entity_id:
                entity_id = UUID(entity_id)
                active_server = get_object_or_404(Server, id=entity_id)
                if active_server not in request.user.get_accessible_servers():
                    raise PermissionDenied()
            else:
                active_server = request.user.active_server

            parameter = f"{active_server.domain}:{active_server.port}"
            metric = 'restic-up' if source == "backup" else 'is-on'

        elif source == "endpoint":
            if entity_id:
                entity_id = UUID(entity_id)
                active_endpoint = get_object_or_404(Endpoint, id=entity_id)
                if active_endpoint not in request.user.get_accessible_endpoints():
                    raise PermissionDenied()
            else:
                active_endpoint = request.user.active_endpoint

            parameter = active_endpoint.url
            metric = 'monitor-status'

        else:
            return HttpResponseBadRequest("Unknown source")

        prom_query = PromQuery.objects.get(code=metric)
        response = api.generic_call(parameter, prom_query, qtype)

        color = "green" if int(response) == 1 else "red"
        html = render_to_string("frontend/components/status_dot.html", {
            "color": color,
            "dim": "22px",
            "title": f"Status: {'online' if int(response) == 1 else 'offline'}"
        })
        return HttpResponse(html)

    except (ValueError, PromQuery.DoesNotExist):
        return HttpResponseBadRequest("Invalid parameters")


######################################################

################### Endpoints ###################

class ListEndpointsView(LoginRequiredMixin, ListView):
    model = Endpoint
    template_name = "frontend/pages/endpoints.html"

    def get_queryset(self):
        user = self.request.user
        return user.get_accessible_endpoints()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_add_endpoint'] = not self.request.user.out_of_endpoints()
        return context

class DeleteEndpointView(LoginRequiredMixin, DeleteView):
    model = Endpoint
    success_url = reverse_lazy('frontend:endpoints')
    template_name = "frontend/components/endpoint_delete_confirmation.html"

@login_required
@require_GET
def edit_endpoint(request, endpoint_id=None):

    if endpoint_id is None:
        endpoint = None
        if request.user.out_of_endpoints():
            return HttpResponseForbidden("You cannot add other endpoint. Upgrade to PRO to unlock unlimited number of endpoints.")
    else:
        endpoint = get_object_or_404(Endpoint, id=endpoint_id)
    
    
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['user'] = request.user.pk
        form = EndpointForm(data=post_data, files=request.FILES, instance=endpoint,)
        if form.is_valid():
            form.save()
    else:

        form = EndpointForm(instance=endpoint)

    return render(request, 'frontend/components/endpoint_form.html', {
        'form': form,
        'action': '',
    })



######################################################

################### ########################

@login_required
@require_GET
def get_instantaneous_data(request, metric):
    try:
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
        elif source == "backup":
            active_server = request.user.active_server
            assert prom_query.target_system == PromQuery.TargetSystem.RESTIC, "Absent metric for Backup-Server obj."
            parameter = f"{active_server.domain}:{active_server.port}"
        else:
            return HttpResponseBadRequest("Unknown source")
        
        data = api.generic_call(parameter, prom_query, qtype)
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse("None", status=400)

@login_required
@require_GET
def get_range_data(request, metric, step=900):
    try:

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
        elif source == "backup":
            assert prom_query.target_system == PromQuery.TargetSystem.RESTIC, "Absent metric for Backup-Server obj."
            if all:
                parameter = user.get_accessible_servers_string()
            else:
                active_entity = request.user.active_server
                parameter = f"{active_entity.domain}:{active_entity.port}"

        
        date_filter = user.get_active_date_filters()
        range_suffix = api._generate_range_suffix(date_filter['date_from'], date_filter['date_to'], step)

        data = api.generic_call(parameter, prom_query, qtype, range_suffix)
        labels = [datetime.fromtimestamp(v[0]).isoformat() for v in data]
        values = [float(v[1]) for v in data]
        return JsonResponse({"labels": labels, "values": values, "title": prom_query.title})
    except Exception as e:
        return JsonResponse({"error": "Metric not found"}, status=400)
