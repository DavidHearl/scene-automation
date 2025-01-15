from django.urls import path
from . import views

app_name = 'manuals'

urlpatterns = [
    path('', views.manual, name='manual'),
    # Technical
    path('folder_structure/', views.folder_structure, name='folder_structure'),
    path('data_storage/', views.data_storage, name='data_storage'),
    # Scanner
    path('scanner_settings/', views.scanner_settings, name='scanner_settings'),
    path('cleaning_scanner/', views.cleaning_scanner, name='cleaning_scanner'),
    # Stream
    path('connecting_to_wifi/', views.connecting_to_wifi, name='connecting_to_wifi'),
    path('file_names/', views.file_names, name='file_names'),
    # Scene
    path('scene_settings/', views.scene_settings, name='scene_settings'),
    path('processing/', views.processing, name='processing'),
    path('registration/', views.registration, name='registration'),
    path('cleaning/', views.cleaning, name='cleaning'),
    path('point_cloud/', views.point_cloud, name='point_cloud'),
    path('exporting/', views.exporting, name='exporting'),
]