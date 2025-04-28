from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request, path):
    return render(request, 'frontend/index.html', {
        'path':path
    })

def hello_world(request):
    assert request.htmx, "Not authorized request!"
    return render(request, 'frontend/hello_world.html', {
    })