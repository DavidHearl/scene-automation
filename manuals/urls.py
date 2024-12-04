from django.urls import path
from . import views

app_name = 'manuals'

urlpatterns = [
    path('', views.manual, name='manual'),
    path('connecting_to_wifi/', views.connecting_to_wifi, name='connecting_to_wifi'),
]