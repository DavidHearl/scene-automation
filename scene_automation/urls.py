from django.contrib import admin
from django.urls import path
from front_end.views import ships_and_areas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', ships_and_areas, name='ships_and_areas')
]
