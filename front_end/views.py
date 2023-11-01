from django.shortcuts import render, HttpResponse
from .models import Ship, Area


def ships_and_areas(request):
    ships = Ship.objects.all()
    areas = Area.objects.all()

    context = {
        'ships': ships,
        'areas': areas,
    }

    return render(request, 'front_end/front_end.html', context)
