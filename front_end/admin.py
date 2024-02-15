from django.contrib import admin
from .models import Ship, Area

class ShipAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'contract_number',
        'company',
    )

class AreaAdmin(admin.ModelAdmin):
    list_display = (
        'ship',
        'area_name',
        'scans',
        'point_cloud_size',
        'machine'

    )
    list_filter = ('ship',)  # Add a filter for 'ship'

admin.site.register(Ship, ShipAdmin)
admin.site.register(Area, AreaAdmin)
