import uuid
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'frontend'

urlpatterns = [

    


    path("api/inst-data/<str:metric>/", views.get_instantaneous_data, name="get_instantaneous_data"),
    path("api/range-data/<str:metric>/", views.get_range_data, name="get_range_data"),
    path("api/inst-data/is-on", views.get_server_status, name="get_server_status"),
    
    path('servers/<uuid:pk>/edit/', views.UpdateServerView.as_view(), name="server_edit"),
    path('servers/create/', views.CreateServerView.as_view(), name="server_create"),
    path('servers/<uuid:pk>/delete/', views.DeleteServerView.as_view(), name="server_delete"),
    
    path('set-active-server/', views.set_active_server, name='set_active_server'),
    path('set-date-range/', views.set_date_range, name='set_date_range'),


    # path("server-status/<uuid:pk>/", views.get_server_status, name="get_server_status"),
    path('mybox/', views.my_box, name="my-box"),

]


page_urlpatterns = [
    re_path(r'^(dashboard/)?$', views.dashboard, name="dashboard"),
    path('resources/', views.resources, name="resources"),
    path('network/', views.network, name="network"),
    path('backup/', views.backup, name="backup"),
    path('report/', views.report, name="report"),
    path('servers/', views.ListServersView.as_view(), name="servers"),
]

urlpatterns += page_urlpatterns
