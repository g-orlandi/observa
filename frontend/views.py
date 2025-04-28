from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request, path):
    return render(request, 'frontend/index.html', {
        'path':path
    })