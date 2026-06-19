from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Invoice
from .forms import InvoiceForm
from services.models import ServiceRecord
from django.db.models import Q
from decimal import Decimal
import datetime

# List all invoices
@login_required
def invoice_list(request):
    query = request.GET.get('q', '')
    payment_status = request.GET.get('status', '')
    
    # Customer can only view their own invoices
    if request.user.role == 'customer':
        try:
            customer = request.user.customer
            invoices = Invoice.objects.filter(service_record__vehicle__customer=customer).order_by('-invoice_date')
        except Exception:
            invoices = Invoice.objects.none()
    else:
        invoices = Invoice.objects.all().order_by('-invoice_date')
        
    if payment_status:
        invoices = invoices.filter(payment_status=payment_status)
        
    if query:
        invoices = invoices.filter(
            Q(id__icontains=query) |
            Q(service_record__vehicle__vehicle_number__icontains=query) |
            Q(service_record__vehicle__customer__customer_name__icontains=query)
        )
        
    return render(request, 'billing/invoice_list.html', {
        'invoices': invoices,
        'query': query,
        'payment_status': payment_status
    })


# Create an invoice
@login_required
@role_required('admin')
def invoice_create(request):
    service_id = request.GET.get('service_record')
    initial_data = {'invoice_date': datetime.date.today()}
    
    if service_id:
        initial_data['service_record'] = service_id
        # We can also pre-calculate parts charges for display purposes
        
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            service_record = invoice.service_record
            
            # Calculate parts charges dynamically from associated PartsUsage
            parts_used = service_record.parts_used.all()
            parts_total = sum(Decimal(p.spare_part.price) * p.quantity_used for p in parts_used)
            
            invoice.parts_charges = parts_total
            invoice.total_amount = invoice.service_charges + invoice.parts_charges
            invoice.save()
            
            messages.success(request, f"Invoice generated successfully. Total: ${invoice.total_amount}")
            return redirect('billing:invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm(initial=initial_data)
        
    return render(request, 'billing/invoice_form.html', {'form': form, 'title': 'Generate Invoice'})


# Detail / Print Invoice view
@login_required
def invoice_detail(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    
    # Customer verification
    if request.user.role == 'customer':
        try:
            customer = request.user.customer
            if invoice.service_record.vehicle.customer != customer:
                messages.error(request, "Permission denied.")
                return redirect('customers:customer_dashboard')
        except Exception:
            return redirect('accounts:profile')
            
    parts_usages = invoice.service_record.parts_used.all()
    return render(request, 'billing/invoice_detail.html', {
        'invoice': invoice,
        'parts_usages': parts_usages
    })


# Quick pay view to mark invoice as Paid
@login_required
@role_required('admin')
def invoice_pay(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.payment_status = 'paid'
    invoice.save()
    messages.success(request, f"Invoice #{invoice.id} marked as Paid.")
    return redirect('billing:invoice_detail', pk=invoice.pk)


# Delete Invoice
@login_required
@role_required('admin')
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if request.method == 'POST':
        invoice.delete()
        messages.success(request, "Invoice deleted successfully.")
        return redirect('billing:invoice_list')
    return render(request, 'billing/invoice_confirm_delete.html', {'invoice': invoice})
