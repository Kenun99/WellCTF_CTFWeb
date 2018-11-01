from django.urls import path
from . import views

urlpatterns = [
    path(r'login/', views.login_user, name='login'),
    path(r'logout/', views.logout_user, name='logout'),
    path(r'register/', views.register_user, name='register'),
    path(r'profile/', views.profile, name='profile'),
    path(r'profile/setting', views.setting, name='setting'),
    path(r'profile/feedback', views.feedback, name='feedback'),

]
