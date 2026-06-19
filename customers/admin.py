from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'phone', 'email', 'user']
    search_fields = ['customer_name', 'phone', 'email']
