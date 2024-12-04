from django.shortcuts import render
from django.http import HttpResponse

def manual(request):
    return render(request, 'manuals/manual.html')

def connecting_to_wifi(request):
    return render(request, 'manuals/connecting_to_wifi.html')


    