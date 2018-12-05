from django.urls import path
from . import views

urlpatterns = [
    path('teamIndex/', views.team, name='teamIndex'),
    path('teamAdd/', views.teamAdd, name='teamAdd'),
    path('teamCreate/', views.teamCreate, name='teamCreate'),
    path('teamDelete/', views.teamDelete, name='teamDelete'),
    path('confirmAddTeam/', views.confirmAddTeam, name='confirmAddTeam'),
]
