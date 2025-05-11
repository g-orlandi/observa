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
    path('endpoints/', views.ListEndpointsView.as_view(), name='endpoints'),
]

endpoints_urlpattern = [
    path('endpoint/<uuid:endpoint_id>/change/', views.edit_endpoint, name="change_endpoint"),
    path('endpoint/add/', views.edit_endpoint, name="add_endpoint"),
    # path('endpoints/create/', views.CreateEndpointView.as_view(), name='endpoint_create'),
    # path('endpoints/update/<uuid:pk>/', views.UpdateEndpointView.as_view(), name='endpoint_update'),
    path('endpoints/<uuid:pk>/delete/', views.DeleteEndpointView.as_view(), name='delete_endpoint'),
]

urlpatterns += page_urlpatterns
urlpatterns += endpoints_urlpattern

