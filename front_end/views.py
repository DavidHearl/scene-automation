from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count
from .models import Ship, Area
from .forms import ShipForm, AreaForm


def ships_and_areas(request):
    # Calculate the total scans for all areas
    total_scans = Area.objects.aggregate(total_scans=Sum('scans'))['total_scans'] or 0

    # Calculate the number of ships
    num_ships = Ship.objects.count()
    num_areas = Area.objects.count()

    # Calculate the average areas per ship
    avg_areas_per_ship = round(num_areas / num_ships, 0)

    # Calculate the average scans per ship
    avg_scans_per_ship = round(total_scans / num_ships, 0)

    avg_completion_time = round(avg_scans_per_ship * 20)
    avg_completion_time = round(avg_completion_time / (60 * 8), 1)

    total_estimated_completion_for_all_ships = Ship.total_estimated_completion_for_all_ships()

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
        'total_scans': total_scans,
        'num_ships': num_ships,
        'num_areas': num_areas,
        'avg_areas_per_ship': avg_areas_per_ship,
        'avg_scans_per_ship': avg_scans_per_ship,
        'avg_completion_time': avg_completion_time,
        'total_estimated_completion_for_all_ships': total_estimated_completion_for_all_ships,
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
