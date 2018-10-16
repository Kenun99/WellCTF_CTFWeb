from django.urls import path
from . import views

urlpatterns = [
    path(r'', views.disscuss, name='writeup')
]