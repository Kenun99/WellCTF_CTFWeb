from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path(r'contests/', views.contests, name='contests'),
    path(r'problems/', views.get_problems, name='problems'),
    path(r'problems/<int:type>', views.get_problems, name='problems'),
    path(r'flagPost', views.flagPost, name='flagPost'),
    path(r'contest_detail/<int:contest_id>', views.contest_detail, name='contest_detail'),
    path(r'contest_detail/board/<int:contest_id>', views.board, name='board'),
]
