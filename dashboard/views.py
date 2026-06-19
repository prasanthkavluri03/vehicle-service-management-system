from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required
from customers.models import Customer
from vehicles.models import Vehicle
from appointment.models import Appointment
from services.models import ServiceRecord
from billing.models import Invoice
from django.db.models import Sum
from django.db.models.functions import ExtractMonth
from decimal import Decimal
import datetime
import json

# Public Homepage View
def home(request):
    if request.user.is_authenticated:
        return redirect('accounts:login_redirect')
    return render(request, 'home.html')


# Admin Dashboard Analytics View
@login_required
@role_required('admin')
def index(request):
    # Summary Metrics
    total_customers = Customer.objects.count()
    total_vehicles = Vehicle.objects.count()
    total_appointments = Appointment.objects.count()
    
    revenue_sum = Invoice.objects.filter(payment_status='paid').aggregate(total=Sum('total_amount'))
    total_revenue = revenue_sum['total'] or Decimal('0.00')
    
    pending_services = ServiceRecord.objects.filter(status__in=['pending', 'ongoing']).count()
    
    # Recent Activities Lists
    recent_appointments = Appointment.objects.all().order_by('-id')[:5]
    recent_services = ServiceRecord.objects.all().order_by('-id')[:5]
    recent_invoices = Invoice.objects.all().order_by('-id')[:5]
    
    # Chart 1: Appointment Status Distribution
    status_counts = {
        'pending': Appointment.objects.filter(status='pending').count(),
        'approved': Appointment.objects.filter(status='approved').count(),
        'in_progress': Appointment.objects.filter(status='in_progress').count(),
        'completed': Appointment.objects.filter(status='completed').count(),
        'cancelled': Appointment.objects.filter(status='cancelled').count(),
    }
    
    # Chart 2: Revenue over current year months
    today = datetime.date.today()
    monthly_rev_query = Invoice.objects.filter(
        payment_status='paid',
        invoice_date__year=today.year
    ).annotate(month=ExtractMonth('invoice_date')).values('month').annotate(total=Sum('total_amount')).order_by('month')
    
    revenue_data = [0] * 12
    for item in monthly_rev_query:
        m_idx = item['month'] - 1
        if 0 <= m_idx < 12:
            revenue_data[m_idx] = float(item['total'])
            
    months_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    return render(request, 'dashboard/index.html', {
        # KPI widgets
        'total_customers': total_customers,
        'total_vehicles': total_vehicles,
        'total_appointments': total_appointments,
        'total_revenue': total_revenue,
        'pending_services': pending_services,
        
        # Recent Tables
        'recent_appointments': recent_appointments,
        'recent_services': recent_services,
        'recent_invoices': recent_invoices,
        
        # Chart JSON
        'status_counts_json': json.dumps(list(status_counts.values())),
        'status_labels_json': json.dumps([s.replace('_', ' ').title() for s in status_counts.keys()]),
        'revenue_data_json': json.dumps(revenue_data),
        'months_labels_json': json.dumps(months_labels),
    })
