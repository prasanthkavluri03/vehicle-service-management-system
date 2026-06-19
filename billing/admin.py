from django.contrib import admin
from .models import Invoice

@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'service_record', 'service_charges', 'parts_charges', 'total_amount', 'payment_status', 'invoice_date']
    search_fields = ['id', 'service_record__id', 'service_record__vehicle__vehicle_number']
    list_filter = ['payment_status', 'invoice_date']
