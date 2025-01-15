from django.shortcuts import render
from django.http import HttpResponse

def manual(request):
    return render(request, 'manuals/manual.html')

# Technical
def folder_structure(request):
    return render(request, 'manuals/folder_structure.html')

def data_storage(request):
    return render(request, 'manuals/data_storage.html')

# Scanner
def scanner_settings(request):
    return render(request, 'manuals/scanner_settings.html')

def cleaning_scanner(request):
    return render(request, 'manuals/cleaning_scanner.html')

# Stream
def connecting_to_wifi(request):
    return render(request, 'manuals/connecting_to_wifi.html')

def file_names(request):
    return render(request, 'manuals/file_names.html')

# Scene
def scene_settings(request):
    return render(request, 'manuals/scene_settings.html')

def processing(request):
    return render(request, 'manuals/processing.html')

def registration(request):
    return render(request, 'manuals/registration.html')

def cleaning(request):
    return render(request, 'manuals/cleaning.html')

def point_cloud(request):
    return render(request, 'manuals/point_cloud.html')

def exporting(request):
    return render(request, 'manuals/exporting.html')
    