from django.contrib import admin
from .models import ServiceRecord, PartsUsage

@admin.register(ServiceRecord)
class ServiceRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'vehicle', 'technician', 'service_date', 'status']
    search_fields = ['vehicle__vehicle_number', 'technician__name', 'description']
    list_filter = ['status', 'service_date']

@admin.register(PartsUsage)
class PartsUsageAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_record', 'spare_part', 'quantity_used']
    search_fields = ['service_record__id', 'spare_part__part_name']
