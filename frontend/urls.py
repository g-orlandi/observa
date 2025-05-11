import uuid
from django.urls import path, re_path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'frontend'

urlpatterns = [
    path("api/inst-data/entity-status/", views.get_entity_status, name="get_entity_status"),

    path("api/inst-data/<str:metric>/", views.get_instantaneous_data, name="get_instantaneous_data"),
    path("api/range-data/<str:metric>/", views.get_range_data, name="get_range_data"),

    
    path('set-active-server/', views.set_active_server, name='set_active_server'),
    path('set-active-endpoint/', views.set_active_endpoint, name='set_active_endpoint'),
    path('set-date-range/', views.set_date_range, name='set_date_range'),

    path('mybox/', views.my_box, name="my-box"),

    path('api/online-entities/', views.get_online_entities, name='get_online_entities'),

]

page_urlpatterns = [
    re_path(r'^(dashboard/)?$', views.dashboard, name="dashboard"),
    path('resources/', views.resources, name="resources"),
    path('network/', views.network, name="network"),
    path('backup/', views.backup, name="backup"),
    path('report/', views.report, name="report"),
    path('servers/', views.ListServersView.as_view(), name="servers"),
    path('endpoints/', views.ListEndpointsView.as_view(), name='endpoints'),
]

servers_urlpattern = [
    path('servers/<uuid:pk>/edit/', views.UpdateServerView.as_view(), name="server_edit"),
    path('servers/create/', views.CreateServerView.as_view(), name="server_create"),
    path('servers/<uuid:pk>/delete/', views.DeleteServerView.as_view(), name="server_delete"),
]

endpoints_urlpattern = [
    path('endpoints/create/', views.CreateEndpointView.as_view(), name='endpoint_create'),
    path('endpoints/update/<uuid:pk>/', views.UpdateEndpointView.as_view(), name='endpoint_update'),
    path('endpoints/delete/<uuid:pk>/', views.DeleteEndpointView.as_view(), name='endpoint_delete'),
]

urlpatterns += page_urlpatterns
urlpatterns += servers_urlpattern
urlpatterns += endpoints_urlpattern

