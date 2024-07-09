# Standard library imports
import calendar
import datetime
from datetime import timedelta, date
from functools import wraps
import time

# Related third party imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models import Sum, Count, F
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.core.serializers import serialize
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404

# Local application/library specific imports
from .forms import *
from .models import *


# --------------------------------------------------------------------------- #
# ------------------------------- Decorators -------------------------------- #
# --------------------------------------------------------------------------- #

# Decorator to measure the time taken by a function
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time} seconds")
        return result
    return wrapper

# --------------------------------------------------------------------------- #
# ------------------------------- Constants --------------------------------- #
# --------------------------------------------------------------------------- #

# Constants to define the time taken for each process
time_per_scan = 20
time_per_area = 35

# Error times
error_codes = ["Minor Fail", "Major Fail", "Critical Fail"]
error_times = [2, 2.45, 2.9]

# Constants to define the number of hours in a workday
hours_per_workday = 7.5

# Constant to define the time added for complexity of the area
exponential_factor = 1.006 # 0.6% increase in time per scan

# Processes and their respective weightings
process_stage = ["processed", "registered", "cleaned", "point_cloud", "exported", "uploaded"]
process_weighting = [15, 40, 15, 10, 15, 5]

# Define the complete status'
completed_statuses = ["Completed", "Legacy", "No Data", "Not Required"]

# Assign Priority to each status
status_priority = {
    "Completed": 0.01,
    "WIP": 0.02,
    "Queued": 0.03,
    "Minor Fail": 0.04,
    "Major Fail": 0.05,
    "Hold": 0.06,
    "Critical Fail": 0.07
}

attributes = ['uploaded', 'exported', 'point_cloud', 'cleaned', 'registered', 'processed']

# --------------------------------------------------------------------------- #
# ------------------------------- Functions --------------------------------- #
# --------------------------------------------------------------------------- #

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
                if area.time_remaining != 0:
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

    return round(total_time, 2)

# --------------------------------------------------------------------------- #
# --------------------------------- Views ----------------------------------- #
# --------------------------------------------------------------------------- #

@timing_decorator
def dashboard(request):
    statistics = Statistics.objects.get(id=8)

    total_time = float(statistics.total_time)
    lower_bound = total_time
    upper_bound = (total_time * 1.3) - lower_bound

    live_scanning_data = Storage.objects.get(id=1)
    scanning_nas = Storage.objects.get(id=2)

    context = {
        'live_scanning_data': live_scanning_data,
        'scanning_nas': scanning_nas,
        'statistics': statistics,
        'lower_bound': lower_bound,
        'upper_bound': upper_bound,
    }

    return render(request, 'front_end/dashboard.html', context)   

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
    machines = Machine.objects.all()

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

    # Initialize total_stars to 0
    total_stars = 0

    # Calculate the complete percentage, total scans, and total stars per ship
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

        # Add the stars count of the current ship to the total stars
        total_stars += ship.stars  # Use ship.stars directly

    # Update statistics.total_stars with the new total stars count
    statistics.total_stars = total_stars
    statistics.save()

    # Star Percentage
    star_percentage = round((total_stars / num_areas) * 100, 4)

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
        'machines': machines,
        'num_ships': num_ships,
        'num_areas': num_areas,
        'today': today,
        'ship_form': ship_form,
        'star_percentage': star_percentage,
    }

    return render(request, 'front_end/front_end.html', context)


def ship_detail(request, ship_id):
    ship = get_object_or_404(Ship, pk=ship_id)
    areas = Area.objects.filter(ship=ship).order_by('area_name')

    queued_areas = [area for area in areas if area.uploaded == "Queued"]
    not_required_areas = [area for area in areas if area.uploaded == "Not Required"]
    other_areas = [area for area in areas if area.uploaded != "Not Required" and area.uploaded != "Queued"]

    sorted_ship_areas = queued_areas + other_areas + not_required_areas

    for area in sorted_ship_areas:
        area.star = (
            area.raw_size != 0.00 and 
            area.processed_size != 0.00 and 
            area.exported_size != 0.00 and 
            area.point_cloud_size != 0)
        area.save()  # Save the area with the updated star field

    # Since you're directly updating the areas, you might not need areas_with_star for the star calculation anymore
    # But if you still need to pass areas with their star status to the context, you can recreate areas_with_star list:
    areas_with_star = [(area, area.star) for area in sorted_ship_areas]

    # Calculate the number of areas with a star
    num_areas_with_star = sum(1 for area in sorted_ship_areas if area.star)

    # Save the count to the ship model
    ship.stars = num_areas_with_star
    ship.save()
    
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
        'areas': sorted_ship_areas,
        'area_form': area_form,
        'areas_with_star': areas_with_star,
    }

    return render(request, 'front_end/ship_details.html', context)


def booking(request):
    # Get all bookings
    bookings = Booking.objects.all()
    users = User.objects.all()

    # Create a dictionary where the keys are the dates and the values are the classes
    booking_classes = {}
    for booking in bookings:
        delta = booking.end_date - booking.start_date  # as timedelta

        for i in range(delta.days + 1):
            day = booking.start_date + timedelta(days=i)
            key = (day.day, day.month)
            # Use the date and month as the key and the scanner as the value
            booking_classes[key] = booking.scanner

    # Get today's date
    today = date.today()

    # Create a dictionary where the keys are the months and the values are the matrices representing the months' calendars
    year_calendar = {}
    for month in range(1, 13):
        month_calendar = calendar.monthcalendar(2024, month)
        for week in month_calendar:
            for i, day in enumerate(week):
                if day != 0:
                    # Check if the current day and month match today's day and month
                    if day == today.day and month == today.month:
                        week[i] = (day, f"{booking_classes.get((day, month), '')} today")
                    else:
                        week[i] = (day, booking_classes.get((day, month), ''))
        year_calendar[month] = month_calendar

    # Convert the month numbers to their names
    year_calendar = {calendar.month_name[month]: month_calendar for month, month_calendar in year_calendar.items()}

    if request.method == 'POST':
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.save()
            messages.success(request, 'Booking added successfully.')
            return redirect('booking')

    bookings = Booking.objects.order_by('start_date')

    context = {
        'bookings': bookings,
        'year_calendar': year_calendar,
        'booking_form': BookingForm(),
        'users': users,
    }

    return render(request, 'front_end/bookings.html', context)


@timing_decorator
def priority(request):
    # Fetch areas that are not completed or not required
    areas = list(Area.objects.select_related('ship').exclude(uploaded__in=["Completed", "Not Required"]).order_by('area_name'))

    # Calculate the priority of each area
    for area in areas:
        ship_priority = area.ship.priority
        area_priority = area.priority

        ship_area_priority = (ship_priority * 1.1) + area_priority

        for i, attr in enumerate(attributes):
            status = getattr(area, attr)
            if status in status_priority:
                ship_area_priority += status_priority[status] / (10 ** i)
                # Round the ship_area_priority to 10 decimal places
                ship_area_priority = round(ship_area_priority, 8)

                area.calcualted_priority = ship_area_priority

    # Update all areas in a single database query
    Area.objects.bulk_update(areas, ['calcualted_priority'])

    # Order the areas by priority
    areas = sorted(areas, key=lambda x: x.calcualted_priority)

    attribute_priority = {
        "processed": 0.06,
        "registered": 0.05,
        "cleaned": 0.04,
        "point_cloud": 0.03,
        "exported": 0.02,
        "uploaded": 0.01
    }

    context = {
        'areas': areas,
    }

    return render(request, 'front_end/priority.html', context)


def calculator(request):
    statistics = Statistics.objects.get(id=8)

    context = {
        'statistics': statistics,
    }

    return render(request, 'front_end/calculator.html', context)


def training(request):
    return render(request, 'front_end/training.html')


def logs(request):
    logins = PageVisit.objects.all().order_by('-timestamp')

    context = {
        'logins': logins,
    }

    return render(request, 'front_end/logs.html', context)


def data(request):
    statistics = Statistics.objects.get(id=8)
    areas = Area.objects.filter(star=True, scans__lt=100)
    num_areas = len(areas)

    point_cloud_scans = []
    raw_size_scans = []
    processed_size_scans = []
    exported_size_scans = []

    # Setup the Graphs
    for area in areas:
        scans = area.scans
        point_cloud_size = area.point_cloud_size
        raw_size = float(area.raw_size)
        processed_size = float(area.processed_size)
        exported_size = float(area.exported_size)

        point_cloud_scans.append({'x': scans, 'y': point_cloud_size})
        raw_size_scans.append({'x': scans, 'y': raw_size})
        processed_size_scans.append({'x': scans, 'y': processed_size})
        exported_size_scans.append({'x': scans, 'y': exported_size})

    scan_count = [area.scans for area in areas]
    point_cloud_count = [area.point_cloud_size for area in areas]
    raw_size_count = [area.raw_size for area in areas]
    processed_size_count = [area.processed_size for area in areas]
    exported_size_count = [area.exported_size for area in areas]

    total_scans = sum(scan_count)

    average_point = sum(point_cloud_count) / total_scans
    average_point = round(average_point)

    average_raw = sum(raw_size_count) / total_scans
    average_raw = round(average_raw, 2)
    average_processed = sum(processed_size_count) / total_scans
    average_processed = round(average_processed, 2)
    average_exported = sum(exported_size_count) / total_scans
    average_exported = round(average_exported, 2)

    statistics.average_raw_storage_per_ship = average_raw
    statistics.average_processed_storage_per_ship = average_processed
    statistics.average_exported_storage_per_ship = average_exported
    statistics.save()

    context = {
        'statistics': statistics,
        'areas': areas,
        'point_cloud_scans': point_cloud_scans,
        'raw_size_scans': raw_size_scans,
        'processed_size_scans': processed_size_scans,
        'exported_size_scans': exported_size_scans,
        'average_point': average_point,
        'average_raw': average_raw,
        'average_processed': average_processed,
        'average_exported': average_exported,
        'num_areas': num_areas,
    }

    return render(request, 'front_end/data.html', context)


def manual(request):
    return render(request, 'front_end/manual.html')


def settings(request):
    return render(request, 'front_end/settings.html')



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


def edit_booking(request, booking_id):
    if request.user.is_superuser:
        bookings = get_object_or_404(Booking, id=booking_id)
    else:
        bookings = get_object_or_404(Booking, id=booking_id, users=request.user)

    users = User.objects.all() if request.user.is_superuser else User.objects.filter(id=request.user.id)

    if request.method == 'POST':
        print("POST request received")
        modify_form = BookingForm(request.POST, instance=bookings)
        if modify_form.is_valid():
            bookings = modify_form.save()
            messages.success(request, 'Booking edited successfully.')
            return redirect('booking')
        else:
            print("Form is not valid")
            print(modify_form.errors)
    else:
        modify_form = BookingForm(instance=bookings)

    context = {
        'bookings': bookings,
        'modify_form': modify_form,
        'users': users,
    }

    return render(request, 'front_end/bookings.html', context)


def delete_booking(request, booking_id):
    # Get the booking with the given ID
    booking = get_object_or_404(Booking, pk=booking_id)
    booking.delete()
    messages.success(request, 'Booking deleted successfully.')

    return redirect('booking')


def edit_priority(request, area_id):
    area = get_object_or_404(Area, id=area_id)
    ship = area.ship

    if request.method == 'POST':
        ship_priority = request.POST.get('ship-priority')
        area_priority = request.POST.get('area-priority')

        area_form = AreaPriorityForm(request.POST, prefix='area', instance=area)
        ship_form = ShipPriorityForm(request.POST, prefix='ship', instance=ship)
        
        if area_form.is_valid() and ship_form.is_valid():
            area_form.save()
            ship_form.save()
            return redirect('priority')
        else:
            print(area_form.errors)
            print(ship_form.errors)

    else:
        area_form = AreaPriorityForm(instance=area)
        ship_form = ShipPriorityForm(instance=ship)

    context = {
        'area_form': area_form,
        'ship_form': ship_form,
    }

    return render(request, 'front_end/priority.html', context)
