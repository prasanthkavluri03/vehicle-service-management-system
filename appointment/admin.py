from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['customer', 'vehicle', 'appointment_date', 'service_type', 'status']
    search_fields = ['customer__customer_name', 'vehicle__vehicle_number', 'service_type']
    list_filter = ['status', 'service_type', 'appointment_date']
