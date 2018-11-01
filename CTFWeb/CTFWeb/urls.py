from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path(r'', include('index.urls')),
    path(r'index/', include('index.urls')),
    path(r'challenges/', include('challenges.urls')),
    path(r'account/', include('account.urls')),
    path(r'team/', include('team.urls')),
    path(r'writeup/', include('writeup.urls')),
    path(r'admin/', admin.site.urls),
    path(r'captcha/', include('captcha.urls'))
]
