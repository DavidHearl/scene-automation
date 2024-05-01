import time
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db.models import Sum, Count, F
from .models import Ship, Area, Machine, Statistics, Booking
from .forms import ShipForm, AreaForm, MachineForm
from functools import wraps
import datetime
import calendar


# Constants to define the time taken for each process
time_per_scan = 20
time_per_area = 30

# Error times
error_codes = ["Minor Fail", "Major Fail", "Critical Fail"]
error_times = [2, 3.5, 5]

# Constants to define the number of hours in a workday
hours_per_workday = 8

# Constant to define the time added for complexity of the area
exponential_factor = 1.006 # 0.6% increase in time per scan

# Processes and their respective weightings
process_stage = ["processed", "registered", "cleaned", "point_cloud", "exported", "uploaded"]
process_weighting = [15, 40, 15, 10, 15, 5]

# Define the complete status'
completed_statuses = ["Completed", "Legacy", "No Data", "Not Required"]


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


""" Calculate the time to complete an area """
@timing_decorator
def calculate_area_time():
    # Define the ships and statistics
    ships = Ship.objects.all()
    statistics = Statistics.objects.get(id=8)

    # Declare time and count variables
    total_time = 0
    area_count = 0

    # Iterate over all ships
    for ship in ships:
        # Don't iterate through the ship if there is no time remaining
        if ship.completed_percentage != 100:
            # Get all the areas of the ship
            areas = ship.area_set.all()
            # Iterate through each area
            for area in areas:
                # FOR DEBUGGING
                # print(f'{area.time_remaining} {area.area_name}')

                # Don't iterate through the area if there is no time remaining
                if area.uploaded != "Completed":
                    # Increment the area count and set completion percentage to 0
                    complete_percentage = 0
                    area_count += 1

                    # Set the base time required to process an area
                    time_remaining = time_per_area

                    # Get the number of scans
                    number_of_scans = area.scans

                    # Calculate the base time
                    base_time = number_of_scans * time_per_scan

                    # Calculate the exponential
                    exponential = exponential_factor ** number_of_scans

                    # Calculate the exponential time
                    exponential_time = base_time * exponential

                    # Add the exponential time to the time remaining
                    time_remaining += exponential_time

                    # Add time to allow for failures
                    for error in error_codes:
                        # Check if the area has a registered error
                        if area.registered == error:
                            # Multiply the time remaining by the error time
                            time_remaining *= error_times[error_codes.index(error)]

                    # Define the current percentage
                    for i, status in enumerate(process_stage):
                        if getattr(area, status) in completed_statuses:
                            complete_percentage += process_weighting[i]

                    # Calculate the time remaining based on the completion percentage
                    time_remaining *= 1 - (complete_percentage / 100)

                    # Set time remaining based on a workday
                    time_remaining = time_remaining / (60 * hours_per_workday)

                    # Add the time to the area
                    area.time_remaining = time_remaining
                    area.save()

                    # Add a running total
                    total_time += time_remaining

            # Update the statistics
            statistics.total_time = total_time
            statistics.save()

            print(f'total time remaining: {total_time} days for {area_count} areas')


""" Calculate the time required to complete the processing per ship """
@timing_decorator
def calculate_ship_time():
    # Define the ships
    ships = Ship.objects.all()

    # Iterate through each ship
    for ship in ships:
        if ship.completed_percentage != 100:
            # Get all the areas of the ship
            areas = ship.area_set.all() # Get all related parameters using the _set method
            ship_time_remaining = 0

            for area in areas:
                if area.uploaded != "Completed" or "Not Required" or "On Hold":
                    # Add the time remaining for each area to the ship
                    ship_time_remaining += area.time_remaining

            ship.time_remaining = ship_time_remaining
            ship.save()

            print(f'total time remaining: {ship.time_remaining} days for {ship.name}')


""" Calculate the total completion time for all ships """
@timing_decorator
def calculate_overall_statistics():
    # Get all the ships, areas and statistics
    ships = Ship.objects.all()
    areas = Area.objects.all()
    statistics = Statistics.objects.get(id=8)
    
    # Set the total time to 0
    total_time = 0
    
    # Iterate through each ship
    for ship in ships:
        if ship.time_remaining != 0:
            total_time += ship.time_remaining
    
    return round(total_time, 2)

    # Update the statistics
    statistics.total_time = total_time

    # Set total scans to 0
    total_scans = 0

    # Iterate through each area and add the scans to the scan total
    for area in areas:
        if area.scans != 0:
            total_scans += area.scans

    # Update the statistics
    statistics.total_scans = total_scans

    # Save the statistics
    statistics.save()
   

""" Render the main page """
@timing_decorator
def ships_and_areas(request):
    # Use the other functions
    calculate_area_time()
    calculate_ship_time()
    calculate_overall_statistics()

    # Fetch ships and areas
    ships = Ship.objects.all().order_by('completed_percentage')
    areas = Area.objects.all()
    statistics = Statistics.objects.get(id=8)

    total_time = statistics.total_time

    # Calculate the number of ships and areas
    num_ships = ships.count()
    num_areas = areas.count()

    # Calculate the number of weeks and days to add to today's date
    add_week = round(statistics.total_time / 5)
    add_day = round(statistics.total_time) - (add_week * 5)

    # Get today's date
    today = datetime.date.today()

    # Add 2 days to today's date
    today += datetime.timedelta(weeks=add_week, days=add_day)

    # Calculate the complete percentage and total scans per ship
    for ship in ships:
        total_scans_per_ship = 0
        completed_percentage = 0

        if ship.completed_percentage != 100:
            for area in ship.area_set.all():
                total_scans_per_ship += area.scans

                for i, status in enumerate(process_stage):
                    if getattr(area, status) in completed_statuses:
                        completed_percentage += process_weighting[i]

            print(round(completed_percentage / ship.area_set.all().count(), 1))
            ship.completed_percentage = round(completed_percentage / ship.area_set.all().count(), 1)
            ship.total_scans = total_scans_per_ship
            ship.save()

    if request.method == 'POST':
        ship_form = ShipForm(request.POST)
        if ship_form.is_valid():
            ship = ship_form.save(commit=False)
            ship.save()
            messages.success(request, 'Ship added successfully.')
            return redirect('ships_and_areas')

    ship_form = ShipForm()

    context = {
        'ships': ships,
        'areas': areas,
        'statistics': statistics,
        'num_ships': num_ships,
        'num_areas': num_areas,
        'today': today,
        'ship_form': ship_form,
    }

    return render(request, 'front_end/front_end.html', context)


def ship_detail(request, ship_id):
    ship = get_object_or_404(Ship, pk=ship_id)
    areas = Area.objects.filter(ship=ship)

    if request.method == 'POST':
        area_form = AreaForm(request.POST)
        if area_form.is_valid():
            area = area_form.save(commit=False)
            area.ship = ship
            area.save()
            messages.success(request, 'Area added successfully.')
            return redirect('ship_detail', ship_id)

    area_form = AreaForm()

    context = {
        'ship': ship,
        'areas': areas,
        'area_form': area_form,
    }

    return render(request, 'front_end/ship_details.html', context)

# --------------------------------------------------------------------------- #
# ----------------------------- CRUD Operations ----------------------------- #
# --------------------------------------------------------------------------- #

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
            return redirect('ship_detail', area.ship.id)
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

    return render(request, 'front_end/ship_details.html', context)


def delete_area(request, area_id):
    area = get_object_or_404(Area, pk=area_id)
    area.delete()
    messages.success(request, 'Area deleted successfully.')

    return redirect('ships_and_areas')

# --------------------------------------------------------------------------- #
# -------------------------------- Calendar --------------------------------- #
# --------------------------------------------------------------------------- #

def booking(request):
    # Get all bookings
    bookings = Booking.objects.all()

    # Create a dictionary where the keys are the dates and the values are the classes
    booking_classes = {}
    for booking in bookings:
        key = (booking.date.day, booking.date.month)
        # Use the date and month as the key and the scanner as the value
        booking_classes[key] = booking.scanner

    # Create a dictionary where the keys are the months and the values are the matrices representing the months' calendars
    year_calendar = {}
    for month in range(1, 13):
        month_calendar = calendar.monthcalendar(2024, month)
        for week in month_calendar:
            for i, day in enumerate(week):
                if day != 0:
                    week[i] = (day, booking_classes.get((day, month), ''))
        year_calendar[month] = month_calendar

    context = {
        'year_calendar': year_calendar,
    }

    return render(request, 'front_end/bookings.html', context)