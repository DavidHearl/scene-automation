# Standard library imports
import calendar
import datetime
import time
from datetime import timedelta, date
from functools import wraps
from decimal import Decimal

# Related third party imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db.models import Sum, Count, F, Case, When, Value, IntegerField
from django.dispatch import receiver
from django.http import HttpResponseRedirect
from django.core.cache import cache
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
        print(f"{func.__name__} took : {end_time - start_time} seconds")
        return result
    return wrapper

# --------------------------------------------------------------------------- #
# ----------------------------- Cache Models -------------------------------- #
# --------------------------------------------------------------------------- #
@timing_decorator
def get_ships():
    # Check if the ships are in the cache
    ships = cache.get('all_ships')
    
    # If not, query the database and cache the result
    if not ships:
        ships = Ship.objects.all()
        cache.set('all_ships', ships, 3600)  # Cache for 1 hour (3600 seconds)
    
    return ships


@timing_decorator
def get_areas():
    # Check if the ships are in the cache
    areas = cache.get('all_areas')
    
    # If not, query the database and cache the result
    if not areas:
        areas = Area.objects.all()
        cache.set('all_areas', areas, 3600)  # Cache for 1 hour (3600 seconds)
    
    return areas


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

# --------------------------------------------------------------------------- #
# ------------------------------- Functions --------------------------------- #
# --------------------------------------------------------------------------- #

""" Calculate the time to complete an area """
@timing_decorator
def calculations():
    ships = get_ships() # Get all the ships from the
    areas = get_areas() # Get all the areas from the
    statistics = Statistics.objects.get(id=8)   # Get the statistics

    total_time = 0      # Set the total time to 0
    total_scans = 0     # Set the total scans to 0

    for area in areas:              # Iterate through all areas
        total_scans += area.scans   # Add the number of scans to the total scans

    for ship in ships:  # Iterate over all ships
        area_count = 0  # Set the number of areas to 0

        if ship.status == False:            # Don't iterate through the ship if it is completed
            ship_time_remaining = 0         # Set the ship time remaining to 0
            area_set = ship.area_set.all()  # Get all the areas of the ship

            for area in area_set:               # Iterate through each area in the area set
                complete_percentage = 0         # Set completion percentage to 0%
                area_count += 1                 # Increment the area count           
                number_of_scans = area.scans    # Get the number of scans

                base_time = number_of_scans * time_per_scan         # Calculate the starting time
                exponential = exponential_factor ** number_of_scans # Calculate the exponential e.g 1.006^scans
                exponential_time = base_time * exponential          # Multiply the base time by the exponential

                area_time_remaining = time_per_area      # Add the allowance for each area, eg 30 Minutes
                area_time_remaining += exponential_time  # Add the exponential time to the time remainiing

                for error in error_codes:           # Loop through the error codes (defined above)
                    if area.registered == error:    # Check if the area has a registered error
                        area_time_remaining *= error_times[error_codes.index(error)] # Multiply the time remaining by the error time

                for i, status in enumerate(process_stage):              # Loop through the process stages
                    if getattr(area, status) in completed_statuses:     # Check if the status is in the completed statuses
                        complete_percentage += process_weighting[i]     # Add the weighting to the completion percentage

                area_time_remaining *= 1 - (complete_percentage / 100)  # Multiply the time remaining by the completion percentage

                area_time_remaining = area_time_remaining / (60 * hours_per_workday)    # Set time remaining based on a workday
                area.time_remaining = area_time_remaining                               # Assign the time remaining to the area
                area.save()                                                             # Save the area

                ship_time_remaining += area_time_remaining  # Add the area time remaining to the ship time remaining
            
            ship.time_remaining = ship_time_remaining  # Assign the ship time remaining to the ship
            ship.save()                                # Save the ship
        else:
            if ship.time_remaining != 0:
                ship.time_remaining = 0
                ship.save()

    for ship in ships:
        total_time += float(ship.time_remaining)

    # Update the statistics
    statistics.total_time = total_time
    statistics.total_scans = total_scans
    statistics.save()

    return round(total_time, 2)

# --------------------------------------------------------------------------- #
# --------------------------------- Views ----------------------------------- #
# --------------------------------------------------------------------------- #
@timing_decorator
def dashboard(request):
    ships = get_ships()
    areas = get_areas()
    statistics = Statistics.objects.get(id=8)
    
    active_ships = ships.filter(completed_percentage__lt=100)
    active_ships = active_ships.exclude(completed_percentage=0)

    # Calculate the number of ships and areas
    num_ships = ships.count()
    num_areas = areas.count()

    # Query ships and annotate each with the count of related areas
    ships_with_area_count = ships.annotate(area_count=Count('area'))

    # Prepare shipNames and scannedAreas for the template
    shipNames = [ship.name for ship in ships_with_area_count]
    scannedAreas = [ship.area_count for ship in ships_with_area_count]

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
        'active_ships': active_ships,
        'num_ships': num_ships,
        'num_areas': num_areas,
        'shipNames': shipNames,
        'scannedAreas': scannedAreas
    }

    return render(request, 'front_end/dashboard.html', context)   

""" Render the main page """
@timing_decorator
def ships_and_areas(request):
    calculations()

    ships = get_ships()
    areas = get_areas()

    ships = ships.annotate(
        custom_order=Case(
            When(contract_number=0, then=Value(0)),  # 0 comes first
            default=Value(1),  # All other values come after 0
            output_field=IntegerField()
        ),
        completed_order=Case(
            When(completed_percentage=0, then=Value(1)),  # 0% at the bottom
            When(completed_percentage=100, then=Value(1)),  # 100% at the bottom
            default=Value(0),  # All other values come before 0% and 100%
            output_field=IntegerField()
        )
    ).order_by('completed_order', 'completed_percentage', 'custom_order', '-contract_number', 'name')

    # Fetch ships and areas
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

    # Calculate the complete percentage, total scans and total stars per ship
    for ship in ships:
        total_scans_per_ship = 0
        completed_percentage = 0

        # Check to see if there are any areas not required or on hold
        for area in ship.area_set.all():
            if area.uploaded == "Not Required" or area.uploaded == "On Hold":
                ship.contains_not_required = True
                ship.save()
                break

        # Check if the ship has reached the maximum number of stars
        if ship.stars == ship.area_set.all().count():
            ship.max_stars = True
            ship.save()    

        if ship.total_scans != 0:
            if ship.completed_percentage != 100:
                for area in ship.area_set.all():
                    total_scans_per_ship += area.scans

                    for i, status in enumerate(process_stage):
                        if getattr(area, status) in completed_statuses:
                            completed_percentage += process_weighting[i]

                if ship.area_set.all().count() != 0:
                    ship.completed_percentage = round(completed_percentage / ship.area_set.all().count(), 1)

                ship.total_scans = total_scans_per_ship
                ship.save()
        else:
            for area in ship.area_set.all():
                total_scans_per_ship += area.scans

            ship.total_scans = total_scans_per_ship
            ship.save()

        # Add the stars count of the current ship to the total stars
        total_stars += ship.stars

    # Set status to complete of not complete based on the completed percentage
    for ship in ships:
        if ship.completed_percentage == 100:
            ship.status = True
        elif ship.completed_percentage == 0:
            ship.status = True
        else:
            ship.status = False
        ship.save()
    
    # Update statistics.total_stars with the new total stars count
    statistics.total_stars = total_stars
    statistics.save()

    # Star Percentage
    star_percentage = round((total_stars / num_areas) * 100, 2)

    if request.method == 'POST':
        ship_form = ShipForm(request.POST, request.FILES)
        if ship_form.is_valid():
            ship_form.save()
            return redirect('ships_and_areas')
        else:
            print(ship_form.errors)
    else:
        ship_form = ShipForm()

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

    # Define the priority for each status
    status_priority = {
        "WIP": 0,
        "Queued": 1,
        "Minor Fail": 2,
        "Major Fail": 2,
        "Critical Fail": 2,
        "Completed": 3,
        "Hold": 4,
        "Not Required": 5
    }

    # Sort the areas using the custom sort key
    sorted_areas = sorted(areas, key=lambda area: (
        status_priority.get(area.processed, 4),
        status_priority.get(area.registered, 4),
        status_priority.get(area.cleaned, 4),
        status_priority.get(area.point_cloud, 4),
        status_priority.get(area.exported, 4),
        status_priority.get(area.uploaded, 4)
    ))

    for area in sorted_areas:
        area.star = (
            area.raw_size != 0.00 and 
            area.processed_size != 0.00 and 
            area.exported_size != 0.00 and 
            area.point_cloud_size != 0)
        area.save()  # Save the area with the updated star field

    # Since you're directly updating the areas, you might not need areas_with_star for the star calculation anymore
    # But if you still need to pass areas with their star status to the context, you can recreate areas_with_star list:
    areas_with_star = [(area, area.star) for area in sorted_areas]

    # Calculate the number of areas with a star
    num_areas_with_star = sum(1 for area in sorted_areas if area.star)

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
        'areas': sorted_areas,
        'area_form': area_form,
        'areas_with_star': areas_with_star,
    }

    return render(request, 'front_end/ship_details.html', context)


def booking(request):
    # Get all bookings & Users
    bookings = Booking.objects.all()
    users = User.objects.all()
    booking_classes = {}  # Initialize the booking_classes dictionary

    # Determine the year to display
    selected_year = request.GET.get('year', date.today().year)
    selected_year = int(selected_year)

    # Update the booking_classes dictionary to handle the "both" case and overlaps
    for booking in bookings:
        start_date = booking.start_date
        end_date = booking.end_date
        first_day = True
        while start_date <= end_date:
            key = (start_date.year, start_date.month, start_date.day)
            if key not in booking_classes:
                booking_classes[key] = set()
            if booking.scanner == "both":
                booking_classes[key].update(["red", "blue"])
                if first_day:
                    booking_classes[key].update(["start-red", "start-blue"])
            else:
                booking_classes[key].add(booking.scanner)
                if first_day:
                    booking_classes[key].add(f"start-{booking.scanner}")
            if start_date == end_date:
                if booking.scanner == "both":
                    booking_classes[key].update(["end-red", "end-blue"])
                else:
                    booking_classes[key].add(f"end-{booking.scanner}")
            start_date += timedelta(days=1)
            first_day = False

    # Convert sets to space-separated strings
    booking_classes = {k: " ".join(v) for k, v in booking_classes.items()}

    # Get today's date
    today = date.today()

    # Add a flag to each booking indicating if the end date has passed
    for booking in bookings:
        if booking.survey_completed != True:
            if booking.end_date < today:
                booking.survey_completed = True
                booking.save()

    # Create a dictionary where the keys are the months and the values are the matrices representing the months' calendars
    year_calendar = {}
    for month in range(1, 13):
        month_calendar = calendar.monthcalendar(selected_year, month)
        for week in month_calendar:
            for i, day in enumerate(week):
                if day != 0:
                    key = (selected_year, month, day)
                    classes = booking_classes.get(key, "")
                    # Check if the current day and month match today's day and month
                    if day == today.day and month == today.month and selected_year == today.year:
                        classes += " today"
                    week[i] = (day, classes)
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
        else:
            print(booking_form.errors)
    else:
        booking_form = BookingForm()

    bookings = Booking.objects.order_by('start_date')

    context = {
        'bookings': bookings,
        'year_calendar': year_calendar,
        'booking_form': BookingForm(),
        'users': users,
        'selected_year': selected_year,
        'years': [selected_year - 1, selected_year, selected_year + 1],
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

        for i, attr in enumerate(reversed(process_stage)):
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
    ships = get_ships()
    areas = get_areas()

    if request.method == 'POST':
        modify_form = AreaForm(request.POST, instance=area)
        if modify_form.is_valid():
            area = modify_form.save()
            messages.success(request, 'Area edited successfully.')
            return redirect('ship_detail', area.ship.id)
        else:
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

    # Retrieve the current ship value
    original_ship = bookings.ship

    if request.method == 'POST':
        modify_form = BookingForm(request.POST, instance=bookings)
        if modify_form.is_valid():
            bookings = modify_form.save(commit=False)
            # Check if the ship value is present, if not, set it to the original value
            if not bookings.ship:
                bookings.ship = original_ship
            bookings.save()
            messages.success(request, 'Booking edited successfully.')
            return redirect('booking')
        else:
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
