from django.shortcuts import render, HttpResponse
from .models import Ship, Area, Status


def say_hello(request):
    ships = Ship.objects.all()
    areas = Area.objects.all()
    status = Status.objects.all()

    context = {
        'ships': ships,
        'areas': areas,
        'status': status,
    }

    return render(request, 'front_end/front_end.html', context)
