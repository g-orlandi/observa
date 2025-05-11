from django.contrib import admin
from .models import Server, PromQuery, Endpoint

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass

@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin):
    pass

@admin.register(PromQuery)
class PromQueryAdmin(admin.ModelAdmin):
    list_display = ["title", "code", "target_system"]
