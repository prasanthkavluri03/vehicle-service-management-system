from django.db import models
from customers.models import Customer
from vehicles.models import Vehicle

# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    SERVICE_CHOICES = (
        ('general', 'General Maintenance'),
        ('oil_change', 'Oil & Filter Change'),
        ('brakes', 'Brake Repair & Service'),
        ('engine', 'Engine Diagnostics & Tuning'),
        ('alignment', 'Wheel Alignment & Balancing'),
        ('ac', 'Air Conditioning Service'),
        ('electrical', 'Electrical Diagnostics'),
        ('bodywork', 'Body Repair & Detailing'),
    )
    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='appointments')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateTimeField()
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, default='general')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.customer.customer_name} - {self.vehicle.vehicle_number} on {self.appointment_date.date()}"
