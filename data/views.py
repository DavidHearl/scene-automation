import time
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, F
from front_end.models import Ship, Area
from functools import wraps
from django.db.models import Q


# Time in minutes
hours_per_workday = 8
time_per_scan = 20
time_per_area = 60
minor_error_time = 15
major_error_time = 30
critical_error_time = 45
time_per_area_failed = 30


def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds")
        return result
    return wrapper


def area_view(request):
    areas = Area.objects.exclude(Q(scans=0) | Q(point_cloud_size=0))
    max_scans = areas.aggregate(Max('scans'))['scans__max']
    max_point_cloud_size = areas.aggregate(Max('point_cloud_size'))['point_cloud_size__max']
    return render(request, 'data.html', {
        'areas': areas,
        'max_scans': max_scans,
        'max_point_cloud_size': max_point_cloud_size
    })


# @timing_decorator
def calculate_completed_percentage(ship):
    # Move the completed_percentage function logic here
    ship_total_scans = ship.total_scans()

    if ship_total_scans == 0:
        return 0

    percentage = 0

    for area in ship.area_set.all():
        weighting = 0
        process_stage = ["processed", "registered", "cleaned", "point_cloud", "exported", "uploaded"]
        process_weighting = [12.5, 100, 100, 12.5, 75, 100, 500, 100]

        for i, status in enumerate(process_stage):
            if getattr(area, status) == "Completed" or getattr(area, status) == "Legacy" or getattr(area, status) == "No Data":
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
def data_view(request):
    # Fetch ships and areas
    ships = Ship.objects.all().prefetch_related('area_set')
    areas = Area.objects.all()

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
                and all(getattr(area, field) == "Completed" for field in ['processed', 'registered', 'cleaned', 'point_cloud', 'exported', 'uploaded'])
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
        'total_scans': total_scans,
        'num_ships': num_ships,
        'num_areas': num_areas,
        'avg_areas_per_ship': avg_areas_per_ship,
        'avg_scans_per_ship': avg_scans_per_ship,
        'avg_completion_time': avg_completion_time,
        'total_estimated_completion': total_estimated_completion,
    }

    return render(request, 'data/data.html', context)
