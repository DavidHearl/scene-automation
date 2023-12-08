from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from front_end.views import ships_and_areas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ships_and_areas, name='ships_and_areas'),
    path('front_end/', include('front_end.urls')),
    path('accounts/', include('allauth.urls')),
    path('scanning_manual/', include('scanning_manual.urls')),
    path('data/', include('data.urls')),
]
