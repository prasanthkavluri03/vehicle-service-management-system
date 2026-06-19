from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Technician
from .forms import TechnicianForm
from django.db.models import Count, Q

# Import ServiceRecord to show active jobs
from services.models import ServiceRecord

# ----------------- ADMIN VIEWS -----------------

# List technicians with workload tracking (active jobs)
@login_required
@role_required('admin')
def technician_list(request):
    # Annotate technicians with count of jobs that are pending or ongoing
    technicians = Technician.objects.annotate(
        active_jobs=Count(
            'service_records',
            filter=Q(service_records__status__in=['pending', 'ongoing'])
        )
    )
    return render(request, 'technicians/technician_list.html', {'technicians': technicians})


# Create technician
@login_required
@role_required('admin')
def technician_create(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Technician added successfully.")
            return redirect('technicians:technician_list')
    else:
        form = TechnicianForm()
    return render(request, 'technicians/technician_form.html', {'form': form, 'title': 'Add Technician'})


# Update technician
@login_required
@role_required('admin')
def technician_update(request, pk):
    tech = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        form = TechnicianForm(request.POST, instance=tech)
        if form.is_valid():
            form.save()
            messages.success(request, "Technician details updated successfully.")
            return redirect('technicians:technician_list')
    else:
        form = TechnicianForm(instance=tech)
    return render(request, 'technicians/technician_form.html', {'form': form, 'title': 'Update Technician'})


# Delete technician
@login_required
@role_required('admin')
def technician_delete(request, pk):
    tech = get_object_or_404(Technician, pk=pk)
    if request.method == 'POST':
        tech.delete()
        messages.success(request, "Technician deleted successfully.")
        return redirect('technicians:technician_list')
    return render(request, 'technicians/technician_confirm_delete.html', {'technician': tech})


# ----------------- TECHNICIAN VIEWS -----------------

# Technician Dashboard
@login_required
@role_required('technician')
def technician_dashboard(request):
    try:
        tech = request.user.technician
    except Technician.DoesNotExist:
        messages.error(request, "Your account does not have a linked Technician profile.")
        return redirect('accounts:profile')
        
    active_services = ServiceRecord.objects.filter(technician=tech).exclude(status='completed').order_by('-service_date')
    completed_services = ServiceRecord.objects.filter(technician=tech, status='completed').order_by('-service_date')
    
    return render(request, 'technicians/technician_dashboard.html', {
        'technician': tech,
        'active_services': active_services,
        'completed_services': completed_services,
    })
