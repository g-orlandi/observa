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
from datetime import timedelta
from main import api
from backend.models import Server

@login_required
def dashboard(request, path):
    return render(request, 'frontend/pages/dashboard.html', {
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

@login_required
def single_server_info(request):
    active_server = request.user.active_server
    context = {}

    if active_server:
        inst_data = api.get_instantaneous_data(active_server)

        end = timezone.now().date()
        start = end - timedelta(days=1)

        aggr_data = api.get_aggregated_data(active_server, start, end)

        context.update({
            'inst_data': inst_data,
            'graph_json': mark_safe(json.dumps({
                "labels": aggr_data["labels"],
                "cpu": aggr_data["cpu"],
                "memory": aggr_data["memory"],
                "disk": aggr_data["disk"],
            })),
            'table_data': [
                {
                    "timestamp": aggr_data["labels"][i],
                    "cpu": aggr_data["cpu"][i],
                    "memory": aggr_data["memory"][i],
                    "disk": aggr_data["disk"][i],
                }
                for i in range(len(aggr_data["labels"]))
            ]
        })

    else:
        context['no_active_server'] = True  

    return render(request, 'frontend/pages/single_server_info.html', context)

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

    def form_valid(self, form):
        form.instance.user = self.request.user  
        return super().form_valid(form)

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


@login_required
def load_graphs(request):
    user = request.user
    active_server = user.active_server

    # Recupera e valida le date
    start_date_str = request.GET.get("start_date")
    end_date_str = request.GET.get("end_date")

    if start_date_str:
        start = parse_date(start_date_str)
    else:
        start = timezone.now().date() - timedelta(days=1)

    if end_date_str:
        end = parse_date(end_date_str)
    else:
        end = timezone.now().date()

    # Recupera i dati da Prometheus
    aggr_data = api.get_aggregated_data(active_server, start, end)

    context = {

        "graph_json": mark_safe(json.dumps({
            "labels": aggr_data["labels"],
            "cpu": aggr_data["cpu"],
            "memory": aggr_data["memory"],
            "disk": aggr_data["disk"]
        })),
        'table_data': [
            {
                "timestamp": aggr_data["labels"][i],
                "cpu": aggr_data["cpu"][i],
                "memory": aggr_data["memory"][i],
                "disk": aggr_data["disk"][i],
            }
            for i in range(len(aggr_data["labels"]))
        ]
    }

    return render(request, "frontend/components/graphs.html", context)