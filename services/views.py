from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import ServiceRecord, PartsUsage
from .forms import ServiceRecordForm, PartsUsageForm
from appointment.models import Appointment
from inventory.models import SparePart
from django.db.models import Q

# List service records
@login_required
@role_required('admin', 'technician')
def service_list(request):
    status_filter = request.GET.get('status', '')
    query = request.GET.get('q', '')
    
    # If the user is a technician, show only their assigned services by default, or all if admin
    if request.user.role == 'technician':
        try:
            tech = request.user.technician
            services = ServiceRecord.objects.filter(technician=tech).order_by('-service_date')
        except Exception:
            services = ServiceRecord.objects.none()
    else:
        services = ServiceRecord.objects.all().order_by('-service_date')
        
    if status_filter:
        services = services.filter(status=status_filter)
        
    if query:
        services = services.filter(
            Q(vehicle__vehicle_number__icontains=query) |
            Q(technician__name__icontains=query) |
            Q(vehicle__customer__customer_name__icontains=query)
        )
        
    return render(request, 'services/service_list.html', {
        'services': services,
        'status_filter': status_filter,
        'query': query
    })


# Create service record
@login_required
@role_required('admin', 'technician')
def service_create(request):
    vehicle_id = request.GET.get('vehicle')
    appointment_id = request.GET.get('appointment')
    
    initial_data = {}
    if vehicle_id:
        initial_data['vehicle'] = vehicle_id
        
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST)
        if form.is_valid():
            service_record = form.save()
            
            # If created from an appointment, update appointment status to in_progress or completed
            if appointment_id:
                try:
                    appt = Appointment.objects.get(id=appointment_id)
                    appt.status = 'in_progress'
                    appt.save()
                except Appointment.DoesNotExist:
                    pass
                    
            messages.success(request, "Service record created successfully.")
            return redirect('services:service_detail', pk=service_record.pk)
    else:
        # Pre-fill technician if user is a technician
        if request.user.role == 'technician':
            try:
                initial_data['technician'] = request.user.technician
            except Exception:
                pass
        form = ServiceRecordForm(initial=initial_data)
        
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Create Service Record'})


# View service record detail (job card)
@login_required
def service_detail(request, pk):
    # Customers can view their own vehicle's service records.
    # Technicians and admins can view any.
    service_record = get_object_or_404(ServiceRecord, pk=pk)
    
    if request.user.role == 'customer':
        try:
            customer = request.user.customer
            if service_record.vehicle.customer != customer:
                messages.error(request, "Permission denied.")
                return redirect('customers:customer_dashboard')
        except Exception:
            messages.error(request, "Customer profile not found.")
            return redirect('accounts:profile')
            
    parts_usages = PartsUsage.objects.filter(service_record=service_record)
    parts_form = PartsUsageForm()
    
    return render(request, 'services/service_detail.html', {
        'service_record': service_record,
        'parts_usages': parts_usages,
        'parts_form': parts_form
    })


# Printable Job Card view
@login_required
def job_card(request, pk):
    service_record = get_object_or_404(ServiceRecord, pk=pk)
    
    if request.user.role == 'customer':
        try:
            customer = request.user.customer
            if service_record.vehicle.customer != customer:
                messages.error(request, "Permission denied.")
                return redirect('customers:customer_dashboard')
        except Exception:
            return redirect('accounts:profile')
            
    parts_usages = PartsUsage.objects.filter(service_record=service_record)
    return render(request, 'services/job_card.html', {
        'service_record': service_record,
        'parts_usages': parts_usages
    })


# Update service record
@login_required
@role_required('admin', 'technician')
def service_update(request, pk):
    service_record = get_object_or_404(ServiceRecord, pk=pk)
    
    # Technician validation
    if request.user.role == 'technician':
        try:
            tech = request.user.technician
            if service_record.technician != tech:
                messages.error(request, "You can only edit service records assigned to you.")
                return redirect('technicians:technician_dashboard')
        except Exception:
            return redirect('accounts:profile')
            
    if request.method == 'POST':
        form = ServiceRecordForm(request.POST, instance=service_record)
        if form.is_valid():
            service_record = form.save()
            messages.success(request, "Service record updated successfully.")
            
            # If marked completed and there's a corresponding appointment, update its status
            if service_record.status == 'completed':
                # Attempt to find matching appointment for this vehicle and customer that is in_progress
                Appointment.objects.filter(
                    vehicle=service_record.vehicle, 
                    status='in_progress'
                ).update(status='completed')
                
            if request.user.role == 'technician':
                return redirect('technicians:technician_dashboard')
            return redirect('services:service_detail', pk=service_record.pk)
    else:
        form = ServiceRecordForm(instance=service_record)
    return render(request, 'services/service_form.html', {'form': form, 'title': 'Update Service Record'})


# Delete service record
@login_required
@role_required('admin')
def service_delete(request, pk):
    service_record = get_object_or_404(ServiceRecord, pk=pk)
    if request.method == 'POST':
        service_record.delete()
        messages.success(request, "Service record deleted successfully.")
        return redirect('services:service_list')
    return render(request, 'services/service_confirm_delete.html', {'service_record': service_record})


# Add spare parts usage to service record
@login_required
@role_required('admin', 'technician')
def add_parts_usage(request, pk):
    service_record = get_object_or_404(ServiceRecord, pk=pk)
    
    if request.method == 'POST':
        form = PartsUsageForm(request.POST)
        if form.is_valid():
            usage = form.save(commit=False)
            usage.service_record = service_record
            part = usage.spare_part
            
            # Inventory validation
            if part.quantity >= usage.quantity_used:
                part.quantity -= usage.quantity_used
                part.save()
                usage.save()
                messages.success(request, f"Added {usage.quantity_used} x {part.part_name} to service record.")
            else:
                messages.error(request, f"Insufficient stock for {part.part_name}. Only {part.quantity} left in stock.")
                
    return redirect('services:service_detail', pk=service_record.pk)


# Delete parts usage from service record
@login_required
@role_required('admin', 'technician')
def delete_parts_usage(request, pk):
    usage = get_object_or_404(PartsUsage, pk=pk)
    service_record_id = usage.service_record.id
    
    # Return parts to stock
    part = usage.spare_part
    part.quantity += usage.quantity_used
    part.save()
    
    usage.delete()
    messages.success(request, "Spare part usage removed. Stock has been returned to inventory.")
    return redirect('services:service_detail', pk=service_record_id)
