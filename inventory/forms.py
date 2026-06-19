from django import forms
from .models import SparePart

# Form for managing inventory items
class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['part_name', 'quantity', 'price', 'supplier']
        widgets = {
            'part_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Spare Part Name'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock Count'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Unit Price', 'step': '0.01'}),
            'supplier': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Supplier Info'}),
        }
