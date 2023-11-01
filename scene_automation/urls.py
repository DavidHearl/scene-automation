from django.contrib import admin
from django.urls import path, include
from front_end.views import ships_and_areas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', ships_and_areas, name='ships_and_areas')
]
