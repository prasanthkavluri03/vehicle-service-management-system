from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import Vehicle
from .forms import VehicleForm, CustomerVehicleForm
from django.db.models import Q

# Import service record to show vehicle service history
from services.models import ServiceRecord

# ----------------- ADMIN VEHICLE VIEWS -----------------

# List vehicles with search functionality
@login_required
@role_required('admin')
def vehicle_list(request):
    query = request.GET.get('q', '')
    if query:
        vehicles = Vehicle.objects.filter(
            Q(vehicle_number__icontains=query) |
            Q(brand__icontains=query) |
            Q(model__icontains=query) |
            Q(customer__customer_name__icontains=query)
        )
    else:
        vehicles = Vehicle.objects.all()
    return render(request, 'vehicles/vehicle_list.html', {
        'vehicles': vehicles,
        'query': query
    })


# Create vehicle
@login_required
@role_required('admin')
def vehicle_create(request):
    if request.method == 'POST':
        form = VehicleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle registered successfully.")
            return redirect('vehicles:vehicle_list')
    else:
        form = VehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Register Vehicle'})


# Vehicle Detail (service history)
@login_required
@role_required('admin')
def vehicle_detail(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    # Fetch all completed or relevant service records for this vehicle
    service_history = ServiceRecord.objects.filter(vehicle=vehicle).order_by('-service_date')
    return render(request, 'vehicles/vehicle_detail.html', {
        'vehicle': vehicle,
        'service_history': service_history
    })


# Update vehicle
@login_required
@role_required('admin')
def vehicle_update(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        form = VehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect('vehicles:vehicle_detail', pk=vehicle.pk)
    else:
        form = VehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Update Vehicle'})


# Delete vehicle
@login_required
@role_required('admin')
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully.")
        return redirect('vehicles:vehicle_list')
    return render(request, 'vehicles/vehicle_confirm_delete.html', {'vehicle': vehicle})


# ----------------- CUSTOMER VEHICLE VIEWS -----------------

# Customer add vehicle
@login_required
@role_required('customer')
def customer_vehicle_create(request):
    try:
        customer = request.user.customer
    except Exception:
        messages.error(request, "Customer profile not found.")
        return redirect('accounts:profile')
        
    if request.method == 'POST':
        form = CustomerVehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save(commit=False)
            vehicle.customer = customer
            vehicle.save()
            messages.success(request, "Your vehicle has been registered successfully.")
            return redirect('customers:customer_dashboard')
    else:
        form = CustomerVehicleForm()
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Register Your Vehicle'})


# Customer vehicle service history detail
@login_required
@role_required('customer')
def customer_vehicle_detail(request, pk):
    try:
        customer = request.user.customer
    except Exception:
        messages.error(request, "Customer profile not found.")
        return redirect('accounts:profile')
        
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=customer)
    service_history = ServiceRecord.objects.filter(vehicle=vehicle).order_by('-service_date')
    return render(request, 'vehicles/vehicle_detail.html', {
        'vehicle': vehicle,
        'service_history': service_history
    })


# Customer vehicle update
@login_required
@role_required('customer')
def customer_vehicle_update(request, pk):
    try:
        customer = request.user.customer
    except Exception:
        messages.error(request, "Customer profile not found.")
        return redirect('accounts:profile')
        
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=customer)
    if request.method == 'POST':
        form = CustomerVehicleForm(request.POST, instance=vehicle)
        if form.is_valid():
            form.save()
            messages.success(request, "Vehicle updated successfully.")
            return redirect('customers:customer_dashboard')
    else:
        form = CustomerVehicleForm(instance=vehicle)
    return render(request, 'vehicles/vehicle_form.html', {'form': form, 'title': 'Update Vehicle Details'})


# Customer vehicle delete
@login_required
@role_required('customer')
def customer_vehicle_delete(request, pk):
    try:
        customer = request.user.customer
    except Exception:
        messages.error(request, "Customer profile not found.")
        return redirect('accounts:profile')
        
    vehicle = get_object_or_404(Vehicle, pk=pk, customer=customer)
    if request.method == 'POST':
        vehicle.delete()
        messages.success(request, "Vehicle deleted successfully.")
        return redirect('customers:customer_dashboard')
    return render(request, 'vehicles/vehicle_confirm_delete.html', {'vehicle': vehicle})
