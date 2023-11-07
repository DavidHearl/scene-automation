from django.urls import path
from . import views

urlpatterns = [
    path('edit_area/<int:area_id>/', views.edit_area, name='edit_area'),
    path('delete_area/<int:area_id>/', views.delete_area, name='delete_area'),

]
