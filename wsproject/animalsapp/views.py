from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from datetime import datetime

# Create your views here.

def index(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    
    return render(request, 'index.html')