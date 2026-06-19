from django.db import models

# Invoice Model
class Invoice(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
    )
    service_record = models.ForeignKey('services.ServiceRecord', on_delete=models.CASCADE, related_name='invoices')
    service_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    parts_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    invoice_date = models.DateField()

    def __str__(self):
        return f"Invoice #{self.id} - Service Record #{self.service_record.id} ({self.get_payment_status_display()})"
