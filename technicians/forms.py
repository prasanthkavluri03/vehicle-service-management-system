from django import forms
from .models import Technician

# Form for managing technician profiles
class TechnicianForm(forms.ModelForm):
    class Meta:
        model = Technician
        fields = ['name', 'specialization', 'phone', 'experience']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Technician Name'}),
            'specialization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Brakes, Engines, Electrical'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}),
        }
