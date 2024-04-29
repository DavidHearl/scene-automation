from django.urls import path
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from . import views

urlpatterns = [
    path('edit_area/<int:area_id>/', views.edit_area, name='edit_area'),
    path('delete_area/<int:area_id>/', views.delete_area, name='delete_area'),
    path('ship_detail/<int:ship_id>/', views.ship_detail, name='ship_detail'),
    path('booking/', views.booking, name='booking'),
]
