from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Customer
from .forms import CustomerForm
from django.db.models import Q

# Imports for customer portal queries
from vehicles.models import Vehicle
from appointment.models import Appointment
from billing.models import Invoice

# ----------------- ADMIN VIEWS -----------------

# List customers with search
@login_required
@role_required('admin')
def customer_list(request):
    query = request.GET.get('q', '')
    if query:
        customers = Customer.objects.filter(
            Q(customer_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {
        'customers': customers,
        'query': query
    })


# Create customer
@login_required
@role_required('admin')
def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer created successfully.")
            return redirect('customers:customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Add Customer'})


# Detail customer
@login_required
@role_required('admin')
def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    vehicles = Vehicle.objects.filter(customer=customer)
    appointments = Appointment.objects.filter(customer=customer).order_by('-appointment_date')
    invoices = Invoice.objects.filter(service_record__vehicle__customer=customer).order_by('-invoice_date')
    
    return render(request, 'customers/customer_detail.html', {
        'customer': customer,
        'vehicles': vehicles,
        'appointments': appointments,
        'invoices': invoices
    })


# Update customer
@login_required
@role_required('admin')
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer details updated successfully.")
            return redirect('customers:customer_detail', pk=customer.pk)
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_form.html', {'form': form, 'title': 'Update Customer'})


# Delete customer
@login_required
@role_required('admin')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted successfully.")
        return redirect('customers:customer_list')
    return render(request, 'customers/customer_confirm_delete.html', {'customer': customer})


# ----------------- CUSTOMER VIEWS -----------------

# Customer self-service portal
@login_required
@role_required('customer')
def customer_dashboard(request):
    # Try to find the linked customer profile
    try:
        customer = request.user.customer
    except Customer.DoesNotExist:
        messages.error(request, "Your account does not have a linked Customer profile.")
        return redirect('accounts:profile')
        
    vehicles = Vehicle.objects.filter(customer=customer)
    appointments = Appointment.objects.filter(customer=customer).order_by('-appointment_date')
    invoices = Invoice.objects.filter(service_record__vehicle__customer=customer).order_by('-invoice_date')
    
    return render(request, 'customers/customer_dashboard.html', {
        'customer': customer,
        'vehicles': vehicles,
        'appointments': appointments,
        'invoices': invoices
    })
