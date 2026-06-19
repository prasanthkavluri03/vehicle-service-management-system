from django import forms
from .models import Vehicle

# Form for admin dashboard to manage vehicles
class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['customer', 'vehicle_number', 'brand', 'model', 'year', 'fuel_type']
        widgets = {
            'customer': forms.Select(attrs={'class': 'form-control'}),
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MH-12-AB-1234'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Camry'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2022'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
        }


# Form for customer self-service to add their own vehicles
class CustomerVehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['vehicle_number', 'brand', 'model', 'year', 'fuel_type']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. MH-12-AB-1234'}),
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Camry'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2022'}),
            'fuel_type': forms.Select(attrs={'class': 'form-control'}),
        }
