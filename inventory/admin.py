from django.contrib import admin
from .models import SparePart

@admin.register(SparePart)
class SparePartAdmin(admin.ModelAdmin):
    list_display = ['part_name', 'quantity', 'price', 'supplier']
    search_fields = ['part_name', 'supplier']
    list_filter = ['supplier']
