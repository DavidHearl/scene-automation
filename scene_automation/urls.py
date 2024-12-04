from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from front_end.views import *
from manuals.views import *
from django.conf.urls import handler404, handler500

urlpatterns = [
    path('', lambda request: redirect('account_login')),
    path('admin/', admin.site.urls),
    path('ships_and_areas/', ships_and_areas, name='ships_and_areas'),
    path('front_end/', include('front_end.urls')),
    path('manuals/', include('manuals.urls')),
    path('', include('front_end.urls')),
    path('', include('front_end.urls')),
    path('accounts/', include('allauth.urls')),
    path('trigger-500/', trigger_500),
]

handler404 = 'front_end.views.custom_404'
handler500 = 'front_end.views.custom_500'