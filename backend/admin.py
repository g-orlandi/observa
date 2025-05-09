from django.contrib import admin
from .models import Server, PromQuery

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    pass

@admin.register(PromQuery)
class PromQueryAdmin(admin.ModelAdmin):
    list_display = ["title", "code", "target_system"]
