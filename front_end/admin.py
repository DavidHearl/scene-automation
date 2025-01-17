from django.contrib import admin
from .models import *


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
        'max_error',
        'average_error',
        'min_overlap',
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

class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'ship',
        'start_date',
        'end_date',
        'scanner',
    )

class PageLoggingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'page',
        'timestamp',
    )

class StorageAdmin(admin.ModelAdmin):
    list_display = (
        'server_name',
        'storage_capacity',
        'storage_used',
        'storage_available',
    )

class DesignerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

class ContractManagerAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

class IssueAdmin(admin.ModelAdmin):
    list_display = (
        'issues',
        'date',
    )

admin.site.register(Ship, ShipAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Machine, MachineAdmin)
admin.site.register(Statistics, StatisticsAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(PageVisit, PageLoggingAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Designer, DesignerAdmin)
admin.site.register(ContractManager, ContractManagerAdmin)
admin.site.register(Issue, IssueAdmin)
