from celery import shared_task
from django.core.cache import cache
from .models import Ship, Area

@shared_task
def update_ships_cache():
    ships = Ship.objects.all()
    cache.set('all_ships', ships, 600)  # Cache for 10 Minutes

@shared_task
def update_areas_cache():
    areas = Area.objects.all()
    cache.set('all_areas', areas, 600)  # Cache for 10 Minutes