from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import role_required
from .models import SparePart
from .forms import SparePartForm
from django.db.models import Q

# Import PartsUsage from services to show historical records of usage
from services.models import PartsUsage

# List parts with search and low-stock highlighting
@login_required
@role_required('admin', 'technician')
def part_list(request):
    query = request.GET.get('q', '')
    filter_low_stock = request.GET.get('low_stock', '')
    
    parts = SparePart.objects.all().order_by('part_name')
    
    if query:
        parts = parts.filter(
            Q(part_name__icontains=query) |
            Q(supplier__icontains=query)
        )
        
    if filter_low_stock == 'true':
        parts = parts.filter(quantity__lte=10)
        
    # Count how many parts are low in stock (quantity <= 10)
    low_stock_count = SparePart.objects.filter(quantity__lte=10).count()
    
    return render(request, 'inventory/part_list.html', {
        'parts': parts,
        'query': query,
        'filter_low_stock': filter_low_stock,
        'low_stock_count': low_stock_count
    })


# Add new part to inventory
@login_required
@role_required('admin')
def part_create(request):
    if request.method == 'POST':
        form = SparePartForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Spare part added to inventory.")
            return redirect('inventory:part_list')
    else:
        form = SparePartForm()
    return render(request, 'inventory/part_form.html', {'form': form, 'title': 'Add Spare Part'})


# Edit inventory part
@login_required
@role_required('admin')
def part_update(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        form = SparePartForm(request.POST, instance=part)
        if form.is_valid():
            form.save()
            messages.success(request, "Inventory stock details updated.")
            return redirect('inventory:part_list')
    else:
        form = SparePartForm(instance=part)
    return render(request, 'inventory/part_form.html', {'form': form, 'title': 'Update Spare Part'})


# Delete inventory part
@login_required
@role_required('admin')
def part_delete(request, pk):
    part = get_object_or_404(SparePart, pk=pk)
    if request.method == 'POST':
        part.delete()
        messages.success(request, "Part deleted from inventory.")
        return redirect('inventory:part_list')
    return render(request, 'inventory/part_confirm_delete.html', {'part': part})


# Parts Usage History view
@login_required
@role_required('admin')
def parts_usage_history(request):
    # Fetch all parts usage logs
    usages = PartsUsage.objects.all().order_by('-service_record__service_date')
    return render(request, 'inventory/parts_usage_history.html', {'usages': usages})
