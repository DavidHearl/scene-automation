from django.contrib import admin
from .models import Ship, Area, Status


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
    )


class StatusAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name_plural = 'Status'


admin.site.register(Ship, ShipAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Status, StatusAdmin)
