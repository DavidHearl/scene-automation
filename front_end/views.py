from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import Ship, Area
from .forms import ShipForm, AreaForm


def ships_and_areas(request):
    ships = Ship.objects.all()
    areas = Area.objects.all()

    # Add ship
    if request.method == 'POST':
        ship_form = ShipForm(request.POST)
        if ship_form.is_valid():
            ship = ship_form.save()
            messages.success(request, 'Ship added successfully.')
            return redirect('ships_and_areas')
    else:
        ship_form = ShipForm()

    # Add area
    if request.method == 'POST':
        area_form = AreaForm(request.POST)
        if area_form.is_valid():
            area = area_form.save()
            messages.success(request, 'Area added successfully.')
            return redirect('ships_and_areas')
    else:
        area_form = AreaForm()

    context = {
        'ships': ships,
        'areas': areas,
        'ship_form' : ship_form,
        'area_form' : area_form,
    }

    return render(request, 'front_end/front_end.html', context)


def edit_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    ships = Ship.objects.all()
    areas = Area.objects.all()

    if request.method == 'POST':
        print("POST request received")
        modify_form = AreaForm(request.POST, instance=area)
        if modify_form.is_valid():
            area = modify_form.save()
            messages.success(request, 'Area edited successfully.')
            return redirect('ships_and_areas')
        else:
            print("Form is not valid")
            print(modify_form.errors)
    else:
        modify_form = AreaForm(instance=area)

    context = {
        'ships': ships,
        'areas': areas,
        'modify_form': modify_form,
    }

    return render(request, 'front_end/front_end.html', context)

def delete_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    area.delete()
    messages.success(request, 'Area deleted successfully.')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
