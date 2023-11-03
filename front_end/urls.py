from django.urls import path
from . import views

urlpatterns = [
    path('add_ship/', views.add_ship, name='add_ship'),
    path('add_area/', views.add_area, name='add_area'),
    path('success/', views.success_page, name='success_page'),
]
