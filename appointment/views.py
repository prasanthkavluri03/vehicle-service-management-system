from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Appointment
from .forms import AppointmentForm, AppointmentBookingForm
from django.db.models import Q
from django.utils import timezone

# ----------------- ADMIN VIEWS -----------------

# List all appointments with filters
@login_required
@role_required('admin')
def appointment_list(request):
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')
    
    appointments = Appointment.objects.all().order_by('-appointment_date')
    
    if status_filter:
        appointments = appointments.filter(status=status_filter)
        
    if query:
        appointments = appointments.filter(
            Q(customer__customer_name__icontains=query) |
            Q(vehicle__vehicle_number__icontains=query) |
            Q(service_type__icontains=query)
        )
        
    return render(request, 'appointment/appointment_list.html', {
        'appointments': appointments,
        'status_filter': status_filter,
        'query': query
    })


# Admin create appointment
@login_required
@role_required('admin')
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment created successfully.")
            return redirect('appointment:appointment_list')
    else:
        form = AppointmentForm()
    return render(request, 'appointment/appointment_form.html', {'form': form, 'title': 'Create Appointment'})


# Admin update appointment
@login_required
@role_required('admin')
def appointment_update(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request, "Appointment updated successfully.")
            return redirect('appointment:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
    return render(request, 'appointment/appointment_form.html', {'form': form, 'title': 'Update Appointment'})


# Admin delete appointment
@login_required
@role_required('admin')
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted successfully.")
        return redirect('appointment:appointment_list')
    return render(request, 'appointment/appointment_confirm_delete.html', {'appointment': appointment})


# Admin approve appointment and redirect to Service Record creation
@login_required
@role_required('admin')
def appointment_approve(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    appointment.status = 'approved'
    appointment.save()
    messages.success(request, f"Appointment for {appointment.customer.customer_name} approved. Please assign a technician and create a service record.")
    # Redirect to create service record with query params to pre-fill
    return redirect(f'/services/add/?vehicle={appointment.vehicle.id}&appointment={appointment.id}')


# ----------------- CUSTOMER VIEWS -----------------

# Customer book appointment
@login_required
@role_required('customer')
def customer_appointment_book(request):
    try:
        customer = request.user.customer
    except Exception:
        messages.error(request, "Customer profile not found.")
        return redirect('accounts:profile')
        
    vehicles_exist = customer.vehicles.exists()
    
    if request.method == 'POST':
        form = AppointmentBookingForm(request.POST, customer=customer)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer
            appointment.status = 'pending'
            appointment.save()
            messages.success(request, "Appointment booked successfully! It is currently pending approval.")
            return redirect('customers:customer_dashboard')
    else:
        form = AppointmentBookingForm(customer=customer)
    return render(request, 'appointment/appointment_form.html', {
        'form': form,
        'title': 'Book Service Appointment',
        'vehicles_exist': vehicles_exist
    })


# Customer cancel appointment
@login_required
@role_required('customer')
def customer_appointment_cancel(request, pk):
    try:
        customer = request.user.customer
    except Exception:
        messages.error(request, "Customer profile not found.")
        return redirect('accounts:profile')
        
    appointment = get_object_or_404(Appointment, pk=pk, customer=customer)
    
    if appointment.status == 'pending':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, "Appointment cancelled successfully.")
    else:
        messages.error(request, "Only pending appointments can be cancelled.")
        
    return redirect('customers:customer_dashboard')
