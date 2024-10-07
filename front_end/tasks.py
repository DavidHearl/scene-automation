from celery import shared_task
from django.core.cache import cache
from .models import Ship, Area
import datetime


@shared_task
def update_ships_cache():
    ships = Ship.objects.all()
    cache.set('all_ships', ships, 60)  # Cache for 5 Minutes
    print(f"update_ships_cache ran at {datetime.datetime.now()}")

@shared_task
def update_areas_cache():
    areas = Area.objects.all()
    cache.set('all_areas', areas, 60)  # Cache for 5 Minutes
    print(f"update_ships_cache ran at {datetime.datetime.now()}")