import uuid
from django.urls import path, re_path, include

from . import views

app_name = 'frontend'

urlpatterns = [
    re_path(r'^(dashboard/)?$', views.dashboard, name="dashboard"),
    path('servers/', views.ListServersView.as_view(), name="servers"),
    path('servers/<uuid:pk>/edit/', views.UpdateServerView.as_view(), name="server_edit"),
    path('servers/<uuid:pk>/delete/', views.DeleteServerView.as_view(), name="server_delete"),
]