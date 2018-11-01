from django.shortcuts import render
from django.http import HttpResponse
from datetime import *


# Create your views here.

def index(request):
    return render(request, 'index.html', {'time_now': datetime.now()})