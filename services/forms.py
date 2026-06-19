from django import forms
from .models import ServiceRecord, PartsUsage
from inventory.models import SparePart

# Form for managing service records
class ServiceRecordForm(forms.ModelForm):
    class Meta:
        model = ServiceRecord
        fields = ['vehicle', 'technician', 'service_date', 'description', 'status']
        widgets = {
            'vehicle': forms.Select(attrs={'class': 'form-control'}),
            'technician': forms.Select(attrs={'class': 'form-control'}),
            'service_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


# Form for logging spare parts usage on a service
class PartsUsageForm(forms.ModelForm):
    class Meta:
        model = PartsUsage
        fields = ['spare_part', 'quantity_used']
        widgets = {
            'spare_part': forms.Select(attrs={'class': 'form-control'}),
            'quantity_used': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filter queryset to only display spare parts that are in stock
        self.fields['spare_part'].queryset = SparePart.objects.filter(quantity__gt=0)
