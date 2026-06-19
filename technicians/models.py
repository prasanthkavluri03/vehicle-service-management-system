from django.db import models
from django.conf import settings

# Technician Model
class Technician(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True, related_name='technician')
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    experience = models.PositiveIntegerField(help_text="Years of experience")

    def __str__(self):
        return f"{self.name} ({self.specialization})"
