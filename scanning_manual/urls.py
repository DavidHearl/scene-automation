from django.urls import path
from .views import manual_page

urlpatterns = [
    path('', manual_page, name='manual_page'),
]
