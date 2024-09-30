# Standard library imports
import calendar
import datetime
import time
import re
import math
from datetime import timedelta, date
from functools import wraps
from decimal import Decimal
from collections import defaultdict, Counter

# Related third party imports
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in
from django.db import transaction
from django.db.models import Sum, Count, F, Case, When, Value, IntegerField, Func, Value
from django.db.models.functions import Trunc
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
        cache.set('all_ships', ships, 600)  # Cache for 10 Minutes
    
    return ships


@timing_decorator
def get_areas():
    # Check if the ships are in the cache
    areas = cache.get('all_areas')
    
    # If not, query the database and cache the result
    if not areas:
        areas = Area.objects.all()
        cache.set('all_areas', areas, 600)  # Cache for 10 Minutes
    
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


@timing_decorator
def assign_stars():
    # Fetch all the areas and ships with related objects
    areas = get_areas()
    ships = Ship.objects.prefetch_related('area_set').all()

    # Fetch the statistics
    statistics = Statistics.objects.get(id=8)

    # List to hold areas and ships that need to be updated
    areas_to_update = []
    ships_to_update = []

    # Criteria to decide if an area should have a star
    for area in areas:
        new_star_value = (
            area.point_cloud_size != 0 and
            area.max_error != 0.0 and
            area.average_error != 0.0 and
            area.min_overlap != 0.0 and
            area.created_on is not None and
            area.point_cloud_created_on is not None and
            area.raw_size != 0.00 and 
            area.processed_size != 0.00 and 
            area.exported_size != 0.00 and
            area.exported == "Completed"
        )
        if area.star != new_star_value:
            area.star = new_star_value
            areas_to_update.append(area)

    # Bulk update areas
    Area.objects.bulk_update(areas_to_update, ['star'])

    for ship in ships:
        # Count the number of stars for each ship
        ship_stars = ship.area_set.filter(star=True).count()
        
        # Check if the ship has all stars
        new_max_stars_value = ship_stars == ship.area_set.count()
        
        if ship.stars != ship_stars or ship.max_stars != new_max_stars_value:
            ship.stars = ship_stars
            ship.max_stars = new_max_stars_value
            ships_to_update.append(ship)

    # Bulk update ships
    Ship.objects.bulk_update(ships_to_update, ['stars', 'max_stars'])

    # Update statistics.total_stars to reflect the total number of ship stars
    total_ship_stars = sum(ship.stars for ship in ships)
    if statistics.total_stars != total_ship_stars:
        statistics.total_stars = total_ship_stars

    # Calculate the star percentage
    total_areas = areas.count()
    starred_areas = areas.filter(star=True).count()
    star_percentage = (starred_areas / total_areas) * 100 if total_areas > 0 else 0

    # Update statistics.star_percentage
    statistics.star_percentage = star_percentage

    # Save the updated statistics
    statistics.save()

# --------------------------------------------------------------------------- #
# --------------------------------- Views ----------------------------------- #
# --------------------------------------------------------------------------- #

""" Render the dashboard """
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
    calculations() # Fetch the function to calculate the time to complete an area

    ships = get_ships() # Get all the ships
    areas = get_areas() # Get all the areas

    assign_stars()

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

    # Set status to complete or not complete based on the completed percentage and total scans
    for ship in ships:
        if ship.completed_percentage == 100:
            ship.status = True
        elif ship.completed_percentage == 0:
            if ship.total_scans != 0:
                ship.status = False
            else:
                ship.status = True
        else:
            ship.status = False
        ship.save()

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
    }

    return render(request, 'front_end/front_end.html', context)


def ship_detail(request, ship_id):
    ship = get_object_or_404(Ship, pk=ship_id)
    areas = Area.objects.filter(ship=ship).order_by('area_name')
    bookings = Booking.objects.filter(ship=ship).first()

    if bookings:
        booking_start_date = bookings.start_date    # Assign the start date to a variable
        booking_end_date = bookings.end_date        # Assign the end date to a variable

        # Format the date to this format '12th September'
        formatted_start_date = booking_start_date.strftime('%d %B')
        formatted_end_date = booking_end_date.strftime('%d %B')

        # Add the appropriate suffix for the day (st, nd, rd, th)
        def add_day_suffix(day):
            if 4 <= day <= 20 or 24 <= day <= 30:
                return 'th'
            else:
                return ['st', 'nd', 'rd'][day % 10 - 1]

        # Apply the suffix
        formatted_booking_start_date = booking_start_date.strftime(f'%d{add_day_suffix(booking_start_date.day)} %B')
        formatted_booking_end_date = booking_end_date.strftime(f'%d{add_day_suffix(booking_end_date.day)} %B')
    else:
        formatted_booking_start_date = None
        formatted_booking_end_date = None

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

    # Criteria to decide if an area should have a star
    for area in sorted_areas:
        area.star = (
            area.point_cloud_size != 0 and
            area.max_error != 0.0 and
            area.average_error != 0.0 and
            area.min_overlap != 0.0 and
            area.created_on != None and
            area.point_cloud_created_on != None and
            area.raw_size != 0.00 and 
            area.processed_size != 0.00 and 
            area.exported_size != 0.00
        )
        area.save()  # Save the area with the updated star field

    # Since you're directly updating the areas, you might not need areas_with_star for the star calculation anymore
    # But if you still need to pass areas with their star status to the context, you can recreate areas_with_star list:
    areas_with_star = [(area, area.star) for area in sorted_areas]

    # Calculate the number of areas with a star
    num_areas_with_star = sum(1 for area in sorted_areas if area.star)
    
    if request.method == 'POST':
        area_form = AreaForm(request.POST)
        if area_form.is_valid():
            area = area_form.save(commit=False)
            area.ship = ship
            area.save()
            messages.success(request, 'Area added successfully.')
            return redirect('ship_detail', ship_id)
        else:
            print(area_form.errors)
    else:
        area_form = AreaForm()

    area_form = AreaForm()

    context = {
        'ship': ship,
        'areas': sorted_areas,
        'area_form': area_form,
        'areas_with_star': areas_with_star,
        'booking': booking,
        'formatted_booking_start_date': formatted_booking_start_date,
        'formatted_booking_end_date': formatted_booking_end_date,
    }

    return render(request, 'front_end/ship_details.html', context)


def booking(request):
    # Retrieve all booking and user records from the database
    bookings = Booking.objects.all()
    users = User.objects.all()
    designers = Designer.objects.all()
    contract_managers = ContractManager.objects.all()

    booking_classes = {} # Initialise an empty dictionary to store the CSS classes for booking dates

    selected_year = request.GET.get('year', date.today().year)  # Determine the year to display in the calendar
    selected_year = int(selected_year) # Convert the year to an integer

    # Update the booking_classes dictionary to handle overlapping bookings and special cases
    for booking in bookings:
        start_date = booking.start_date  # The start date of the booking
        end_date = booking.end_date  # The end date of the booking
        first_day = True  # Flag to track the first day of the booking

        # Loop through each day in the booking period
        while start_date <= end_date:
            key = (start_date.year, start_date.month, start_date.day)  # Create a unique key for each day
            if key not in booking_classes:
                booking_classes[key] = set()  # Initialize a set to store CSS classes for this day

            # Handle bookings that cover both "red" and "blue" scanners
            if booking.scanner == "both":
                booking_classes[key].update(["red", "blue"])  # Add both scanner classes
                if first_day:
                    booking_classes[key].update(["start-red", "start-blue"])  # Add start classes on the first day
            else:
                booking_classes[key].add(booking.scanner)  # Add the specific scanner class
                if first_day:
                    booking_classes[key].add(f"start-{booking.scanner}")  # Add start class on the first day

            # If it's the last day of the booking, add end classes
            if start_date == end_date:
                if booking.scanner == "both":
                    booking_classes[key].update(["end-red", "end-blue"])  # Add end classes for both scanners
                else:
                    booking_classes[key].add(f"end-{booking.scanner}")  # Add end class for the specific scanner

            start_date += timedelta(days=1)  # Move to the next day
            first_day = False  # After the first iteration, set this to False

    # Convert each set of CSS classes into a space-separated string
    booking_classes = {k: " ".join(v) for k, v in booking_classes.items()}

    # Get today's date
    today = date.today()

    # Mark bookings as "survey completed" if their end date has passed and the survey is not already completed
    for booking in bookings:
        if booking.survey_completed != True:
            if booking.end_date < today:
                booking.survey_completed = True  # Update the survey_completed field
                booking.save()  # Save the updated booking record

    # Create a dictionary to store the calendar for each month of the selected year
    year_calendar = {}
    for month in range(1, 13):
        month_calendar = calendar.monthcalendar(selected_year, month)  # Get the calendar matrix for the month
        for week in month_calendar:
            for i, day in enumerate(week):
                if day != 0:  # If the day is not part of the previous or next month
                    key = (selected_year, month, day)  # Create a unique key for the day
                    classes = booking_classes.get(key, "")  # Get the CSS classes for the day
                    # Check if the day is today, and if so, add the "today" class
                    if day == today.day and month == today.month and selected_year == today.year:
                        classes += " today"
                    day_id = f"{selected_year:04d}-{month:02d}-{day:02d}"  # Create an ID for the day in "YYYY-MM-DD" format
                    week[i] = (day, classes, day_id)  # Update the day in the calendar matrix with the day, its classes, and its ID
                year_calendar[month] = month_calendar  # Store the updated month calendar in the year calendar

    # Convert month numbers to month names in the year calendar dictionary
    year_calendar = {calendar.month_name[month]: month_calendar for month, month_calendar in year_calendar.items()}

    # Handle POST requests (form submissions)
    if request.method == 'POST':
        if 'booking_form' in request.POST:
            booking_form = BookingForm(request.POST) # Initialize the booking form with POST data
            if booking_form.is_valid():
                booking = booking_form.save(commit=False)
                booking.save()
                messages.success(request, 'Booking added successfully.')
                return redirect('booking')
            else:
                print(booking_form.errors)
        elif 'ship_form' in request.POST:
            ship_form = ShipForm(request.POST, request.FILES)
            if ship_form.is_valid():
                ship_form.save()
                return redirect('booking')
            else:
                print(ship_form.errors)
    else:
        booking_form = BookingForm()
        ship_form = ShipForm()

    # Reorder bookings by start date
    bookings = Booking.objects.order_by('start_date')

    context = {
        'bookings': bookings,
        'year_calendar': year_calendar,
        'booking_form': booking_form,
        'users': users,
        'selected_year': selected_year,
        'years': [selected_year - 1, selected_year, selected_year + 1],
        'ship_form': ship_form,
        'designers': designers,
        'contract_managers': contract_managers,
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


def planning(request):
    areas = Area.objects.all()

    # Words to filter out
    filter_words = ["Cabin", "Restroom", "Toilet", "Embark", "Penthouse"]

    # Count occurrences of each area_name
    area_counter = Counter(area.area_name for area in areas)

    # Filter out areas that occur only once
    filtered_areas = [area for area in areas if area_counter[area.area_name] > 1]

    # Exclude areas with specific values
    filtered_areas = [area for area in filtered_areas if not any(word in area.area_name for word in filter_words)]

    # Group remaining areas by area_name and calculate statistics
    area_dict = defaultdict(lambda: {'ships': [], 'scans': []})
    for area in filtered_areas:
        area_dict[area.area_name]['ships'].append(str(area.ship))  # Ensure ship is a string
        area_dict[area.area_name]['scans'].append(area.scans)  # Assuming 'scans' is a field in Area

    # Format the output with statistics
    formatted_areas = []
    for area_name, data in area_dict.items():
        ships = data['ships']
        scans = data['scans']
        occurrences = len(ships)
        avg_scans = math.ceil(sum(scans) / occurrences) if occurrences > 0 else 0
        min_scans = min(scans) if scans else 0
        max_scans = max(scans) if scans else 0
        ship_list = ", ".join(ships)
        formatted_area = {
            'area_name': area_name,
            'occurrences': occurrences,
            'avg_scans': avg_scans,
            'min_scans': min_scans,
            'max_scans': max_scans,
            'ships': ship_list
        }
        formatted_areas.append(formatted_area)

    # Sort the formatted areas alphabetically by area_name
    formatted_areas.sort(key=lambda x: x['area_name'])

    context = {
        'cleaned_areas': formatted_areas,
    }

    return render(request, 'front_end/planning.html', context)


def logs(request):
    logins = PageVisit.objects.annotate(
        five_minute=Trunc('timestamp', 'minute', interval=5)
    ).order_by('-five_minute', 'user', '-timestamp').distinct('five_minute', 'user')

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
            modify_form.save_m2m()  # Save many-to-many relationships

            # Update contract_manager and designer manually
            bookings.contract_manager.set(request.POST.getlist('contract_managers'))
            bookings.designer.set(request.POST.getlist('designers'))

            messages.success(request, 'Booking edited successfully.')
            return redirect('booking')
        else:
            print(modify_form.errors)
    else:
        modify_form = BookingForm(instance=bookings)

    contract_managers = ContractManager.objects.all()
    designers = Designer.objects.all()

    context = {
        'bookings': bookings,
        'modify_form': modify_form,
        'users': users,
        'contract_managers': contract_managers,
        'designers': designers,
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


# Error Handling
def custom_404(request, exception):
    return render(request, '404.html', status=404)


def custom_500(request):
    return render(request, '500.html', status=500)


def trigger_500(request):
    # This view will raise an exception to trigger a 500 error
    raise Exception("This is a test 500 error")