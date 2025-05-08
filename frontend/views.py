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
from django.views.decorators.http import require_POST
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render
from django.utils.dateparse import parse_date
from django.utils import timezone
from datetime import timedelta, datetime
from main import api
from django.http import JsonResponse, HttpResponseBadRequest


from backend.models import Server, PromQuery
import requests
from main import settings
from requests.auth import HTTPBasicAuth
import re

################### Main pages ###################

@login_required
def dashboard(request, path):
    return render(request, 'frontend/pages/dashboard.html', {
    })

@login_required
def resources(request):
    return render(request, 'frontend/pages/resources.html', {
    })

@login_required
def network(request):
    return render(request, 'frontend/pages/network.html', {
    })

@login_required
def report(request):
    return render(request, 'frontend/pages/report.html', {
    })

@login_required
def backup(request):
    return render(request, 'frontend/pages/backup.html', {
    })

######################################################

# @login_required
# def network(request):
#     active_server = request.user.active_server
#     context = {}

#     if active_server:
#         inst_data = api.instantaneous_network_data(active_server)
#         context.update({
#             'inst_data': inst_data
#         })
#         # inst_data = api.get_instantaneous_data(active_server)

#         # end = timezone.now().date()
#         # start = end - timedelta(days=1)

#         # aggr_data = api.get_aggregated_data(active_server, start, end)

#         # context.update({
#         #     'inst_data': inst_data,
#         #     'graph_json': mark_safe(json.dumps({
#         #         "labels": aggr_data["labels"],
#         #         "cpu": aggr_data["cpu"],
#         #         "memory": aggr_data["memory"],
#         #         "disk": aggr_data["disk"],
#         #     })),
#         #     'table_data': [
#         #         {
#         #             "timestamp": aggr_data["labels"][i],
#         #             "cpu": aggr_data["cpu"][i],
#         #             "memory": aggr_data["memory"][i],
#         #             "disk": aggr_data["disk"][i],
#         #         }
#         #         for i in range(len(aggr_data["labels"]))
#         #     ]
#         # })

#     else:
#         context['no_active_server'] = True  

#     return render(request, 'frontend/pages/network.html', context)

################### Servers list ###################

class ListServersView(LoginRequiredMixin, ListView):
    model = Server
    template_name = "frontend/pages/servers.html"

class UpdateServerView(LoginRequiredMixin, UpdateView):
    model = Server
    fields = ['name', 'description', 'domain', 'port', 'logo']
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/components/update_server_modal.html"

class DeleteServerView(LoginRequiredMixin, DeleteView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    template_name = "frontend/components/delete_server_confirmation_modal.html"

class CreateServerView(LoginRequiredMixin, CreateView):
    model = Server
    success_url = reverse_lazy('frontend:servers')
    fields = ['name', 'description', 'domain', 'port', 'logo']
    template_name = "frontend/components/create_server_modal.html"

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

def get_server_status(request):
    active_server = request.user.active_server
    response = api.get_instantaneous_data(active_server, 'is-on')
    color = "green" if int(response) == 1 else "red"
    html = f'<span style="display:inline-block; width:12px; height:12px; border-radius:50%; background:{color};"></span>'
    return HttpResponse(html)


######################################################

################### Resources ########################

@login_required
def get_instantaneous_data(request, metric):
    active_server = request.user.active_server
    
    try:
        data = api.get_instantaneous_data(active_server, metric)
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse("None")

@login_required
def get_range_data(request, metric):
    user = request.user
    active_server = user.active_server

    date_filter = user.get_active_date_filters()
    start_date = date_filter['date_from']
    end_date = date_filter['date_to']

    print(start_date)
    print(end_date)

    try:
        data = api.get_range_data(active_server, metric, start_date, end_date)
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