from django.urls import path, re_path

from . import views

app_name = 'frontend'

urlpatterns = [
    re_path(r'^(home/)?$', views.index, name="home"),
]