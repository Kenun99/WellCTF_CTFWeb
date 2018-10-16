from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def disscuss(request):
    return HttpResponse('writeup.html')