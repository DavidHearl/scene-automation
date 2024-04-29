from django.contrib import admin
from .models import Ship, Area, Machine, Statistics


class ShipAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'contract_number',
        'company',
        'priority',
    )

class AreaAdmin(admin.ModelAdmin):
    list_display = (
        'ship',
        'area_name',
        'scans',
        'time_remaining',
        'point_cloud_size',
    )
    list_filter = ('ship',)  # Add a filter for 'ship'

class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

class StatisticsAdmin(admin.ModelAdmin):
    list_display = (
        'total_time',
        'total_scans',
        'average_scans_per_ship',
        'average_scans_per_area',
        'average_areas_per_ship',
        'average_completion_time_per_ship',
    )


admin.site.register(Ship, ShipAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Statistics, StatisticsAdmin)
