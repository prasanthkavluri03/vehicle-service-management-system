from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['vehicle_number', 'brand', 'model', 'year', 'fuel_type', 'customer']
    search_fields = ['vehicle_number', 'brand', 'model', 'customer__customer_name']
    list_filter = ['fuel_type', 'year']
