from django.urls import path
from . import views

urlpatterns = [
    path('edit_area/<int:area_id>/', views.edit_area, name='edit_area'),
]
