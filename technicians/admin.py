from django.contrib import admin
from .models import Technician

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'phone', 'experience', 'user']
    search_fields = ['name', 'specialization', 'phone']
