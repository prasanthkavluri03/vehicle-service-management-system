from django.db import models
from vehicles.models import Vehicle
from technicians.models import Technician

# ServiceRecord Model
class ServiceRecord(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='service_records')
    technician = models.ForeignKey(Technician, on_delete=models.CASCADE, related_name='service_records')
    service_date = models.DateField()
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"Service for {self.vehicle.vehicle_number} on {self.service_date} - {self.get_status_display()}"


# PartsUsage Model mapping spare parts consumed during service
class PartsUsage(models.Model):
    service_record = models.ForeignKey(ServiceRecord, on_delete=models.CASCADE, related_name='parts_used')
    spare_part = models.ForeignKey('inventory.SparePart', on_delete=models.CASCADE, related_name='usages')
    quantity_used = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity_used} x {self.spare_part.part_name} for Service Record #{self.service_record.id}"
