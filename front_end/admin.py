from django.contrib import admin
from .models import Ship, Area, Machine


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
        'point_cloud_size',
    )
    list_filter = ('ship',)  # Add a filter for 'ship'

class MachineAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )


admin.site.register(Ship, ShipAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Machine, MachineAdmin)
