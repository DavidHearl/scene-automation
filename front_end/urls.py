from django.urls import path
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from . import views

urlpatterns = [
    path('edit_area/<int:area_id>/', views.edit_area, name='edit_area'),
    path('delete_area/<int:area_id>/', views.delete_area, name='delete_area'),
    path('ship_detail/<int:ship_id>/', views.ship_detail, name='ship_detail'),
    path('booking/', views.booking, name='booking'),
    path('calculator/', views.calculator, name='calculator'),
    path('priority/', views.priority, name='priority'),
    path('planning/', views.planning, name='planning'),
    path('issues/', views.issues, name='issues'),
    path('training/', views.training, name='training'),
    path('edit_priority/<int:area_id>/', views.edit_priority, name='edit_priority'),
    path('logs/', views.logs, name='logs'),
    path('data/', views.data, name='data'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('settings/', views.settings, name='settings'),
    path('delete_booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('edit_booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('issues/delete/<int:issue_id>/', views.delete_issue, name='delete_issue'),
    path('issues/edit/<int:issue_id>/', views.edit_issue, name='edit_issue'),
]
