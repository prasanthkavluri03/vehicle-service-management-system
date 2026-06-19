from django import forms
from .models import Invoice
from services.models import ServiceRecord

# Form to create or edit Invoices
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['service_record', 'service_charges', 'invoice_date', 'payment_status']
        widgets = {
            'service_record': forms.Select(attrs={'class': 'form-control'}),
            'service_charges': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'e.g. 50.00'}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_status': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Limit to service records that don't have an invoice yet, or completed service records
        self.fields['service_record'].queryset = ServiceRecord.objects.all()
