from django.shortcuts import render

def manual_page(request):
    return render(request, 'scanning_manual/manual.html')
