import time
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, F
from .models import Ship, Area, Machine
from .forms import ShipForm, AreaForm, MachineForm
from functools import wraps
import datetime


# Time in minutes
hours_per_workday = 8
time_per_scan = 29
time_per_area = 60
minor_error_time = 15
major_error_time = 30
critical_error_time = 45
time_per_area_failed = 30


""" Decorator to measure the time taken by a function """
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds")
        return result
    return wrapper


""" Calculate the time required to complete the processing per ship """
@timing_decorator
def calculate_completed_percentage(ship):
    # Get the total number of scans for the ship
    ship_total_scans = ship.total_scans()

    if ship_total_scans == 0:
        return 0

    percentage = 0

    for area in ship.area_set.all():
        weighting = 0
        process_stage = ["imported", "processed", "registered", "aligned", "cleaned", "point_cloud", "exported", "uploaded"]
        process_weighting = [12.5, 150, 200, 12.5, 100, 100, 350, 75]

        completed_statuses = ["Completed", "Legacy", "No Data", "Not Required"]

        for i, status in enumerate(process_stage):
            if getattr(area, status) in completed_statuses:
                weighting += process_weighting[i]

        area_percentage = (100 * (weighting/1000) * (int(area.scans) / int(ship_total_scans)))
        percentage += area_percentage

    return round(percentage, 1)


# @timing_decorator
def calculate_estimated_completion(ship):
    total_scans = ship.total_scans()
    completed_percentage = calculate_completed_percentage(ship)
    estimated_time_per_scan = total_scans * time_per_scan / (60 * hours_per_workday)
    total_areas = ship.area_set.count()
    additional_time_per_area = total_areas * (time_per_area / (60 * hours_per_workday))
    total_failure_time = 0
    number_of_failures = 0

    for area in ship.area_set.all():
        if area.registered == "Minor Fail":
            total_failure_time += int(area.scans) * minor_error_time
            number_of_failures += 1
        elif area.registered == "Major Fail":
            total_failure_time += int(area.scans) * major_error_time
            number_of_failures += 1
        elif area.registered == "Critical Fail":
            total_failure_time += int(area.scans) * critical_error_time
            number_of_failures += 1

    total_area_fail_time = (number_of_failures * time_per_area_failed) / (60 * hours_per_workday)
    total_failure_time = (total_failure_time / (60 * hours_per_workday)) + total_area_fail_time
    estimated_time = estimated_time_per_scan + additional_time_per_area + total_failure_time
    multiplier = 1 - (completed_percentage / 100)
    estimated_time *= 0 if multiplier == 0 else multiplier

    return round(estimated_time, 2)


@timing_decorator
def total_estimated_completion_for_all_ships():
    # Iterate over all ships and sum their estimated completion times
    total_estimated_time_for_all_ships = sum(calculate_estimated_completion(ship) for ship in Ship.objects.all())
    return round(total_estimated_time_for_all_ships, 2)


@timing_decorator
def ships_and_areas(request):
    # Fetch ships and areas
    ships = Ship.objects.all().prefetch_related('area_set')
    areas = Area.objects.all()
    machines = Machine.objects.all()

    # Calculate the total scans for all areas using database aggregation
    total_scans = Area.objects.aggregate(total_scans=Sum('scans'))['total_scans'] or 0

    # Calculate the number of ships and areas
    num_ships = ships.count()
    num_areas = areas.count()

    # Calculate the average areas per ship and scans per ship
    avg_areas_per_ship = round(num_areas / num_ships) if num_ships != 0 else 0
    avg_scans_per_ship = round(total_scans / num_ships) if num_ships != 0 else 0

    avg_completion_time = round(avg_scans_per_ship * 20 / (60 * 8), 1)
    
    # Calculate total estimated completion time
    total_estimated_completion = total_estimated_completion_for_all_ships()

    # Calculate the number of weeks and days to add to today's date
    add_week = round(total_estimated_completion / 5)
    add_day = total_estimated_completion - (add_week * 5)

    # Get today's date
    today = datetime.date.today()

    # Add 2 days to today's date
    today += datetime.timedelta(weeks=add_week, days=add_day)

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

    # Add machine
    if request.method == 'POST':
        machine_form = MachineForm(request.POST)
        if machine_form.is_valid():
            machine = machine_form.save()
            messages.success(request, 'Machine added successfully.')
            return redirect('ships_and_areas')
    else:
        machine_form = MachineForm()

    # Calculate completed percentage and estimated completion for each ship
    for ship in ships:
        ship.completed_percentage = calculate_completed_percentage(ship)
        ship.estimated_completion = calculate_estimated_completion(ship)

        # Calculate completion status for each area of the current ship
        for area in ship.area_set.all():
            area.is_completed = (
                area.scans != 0
                and area.point_cloud_size != 0
                and area.raw_size != 0
                and area.processed_size != 0
                and area.exported_size != 0
                and all(getattr(area, field) == "Completed" for field in ['imported', 'processed', 'registered', 'aligned', 'cleaned', 'point_cloud', 'exported', 'uploaded'])
            )


    # Define a sorting key function
    def sorting_key(ship):
        if ship.completed_percentage >= 100:
            return (-4, ship.contract_number)  # Priority is disregarded if completion is 100% or more
        else:
            return (-ship.priority, -ship.completed_percentage, ship.contract_number)

    # Sort ships based on the new sorting key
    sorted_ships = sorted(ships, key=sorting_key, reverse=True)

    context = {
        'ships': sorted_ships,
        'completed_percentages': [ship.completed_percentage for ship in ships],
        'areas': areas,
        'machines': machines,
        'total_scans': total_scans,
        'num_ships': num_ships,
        'num_areas': num_areas,
        'avg_areas_per_ship': avg_areas_per_ship,
        'avg_scans_per_ship': avg_scans_per_ship,
        'avg_completion_time': avg_completion_time,
        'total_estimated_completion': total_estimated_completion,
        'today': today,
        'ship_form': ship_form,
        'area_form': area_form,
        'machine_form': machine_form,
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

@timing_decorator
def delete_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    area.delete()
    messages.success(request, 'Area deleted successfully.')

    return render(request, 'front_end/front_end.html')
