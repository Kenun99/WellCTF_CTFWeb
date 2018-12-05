from django.urls import path
from . import views

urlpatterns = [
    path(r'login/', views.login_user, name='login'),
    path(r'logout/', views.logout_user, name='logout'),
    path(r'register/', views.register_user, name='register'),
    path(r'profile/<int:solved_page>/<int:contest_page>/', views.profile, name='profile'),
    path(r'setting/', views.setting, name='setting'),
    path(r'feedback/', views.feedback, name='feedback'),

]
