from django.db import models

# SparePart Model
class SparePart(models.Model):
    part_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0, help_text="Stock quantity available")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price per unit")
    supplier = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.part_name} (Qty: {self.quantity}, Price: ${self.price})"
