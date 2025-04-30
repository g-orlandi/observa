from django.urls import path, re_path, include

from . import views

app_name = 'frontend'

urlpatterns = [
    re_path(r'^(dashboard/)?$', views.dashboard, name="dashboard"),
    path('servers/', views.servers, name="servers"),
]