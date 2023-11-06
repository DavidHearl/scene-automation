from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import Ship, Area
from .forms import ShipForm, AreaForm


def ships_and_areas(request):
    ships = Ship.objects.all()
    areas = Area.objects.all()

    if request.method == 'POST':
        ship_form = ShipForm(request.POST)
        if ship_form.is_valid():
            ship = ship_form.save()
            messages.success(request, 'Ship added successfully.')
            return redirect('ships_and_areas')  # Redirect to a success page or any other desired URL after submission
    else:
        ship_form = ShipForm()


    if request.method == 'POST':
        area_form = AreaForm(request.POST)
        if area_form.is_valid():
            area = area_form.save()
            messages.success(request, 'Area added successfully.')
            print("Area Form Ship Value:", area_form.cleaned_data['ship'])
            return redirect('ships_and_areas')  # Redirect to a success page or any other desired URL after submission
    else:
        area_form = AreaForm()

    context = {
        'ships': ships,
        'areas': areas,
        'ship_form' : ship_form,
        'area_form' : area_form,
    }

    return render(request, 'front_end/front_end.html', context)
