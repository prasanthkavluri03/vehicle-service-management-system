import os
import django
import datetime
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vehicle_service_management.settings')
django.setup()

from accounts.models import User
from customers.models import Customer
from vehicles.models import Vehicle
from appointment.models import Appointment
from technicians.models import Technician
from services.models import ServiceRecord, PartsUsage
from inventory.models import SparePart
from billing.models import Invoice

def populate():
    # Clear existing data except the superuser 'admin'
    User.objects.exclude(username='admin').delete()
    Customer.objects.all().delete()
    Vehicle.objects.all().delete()
    Appointment.objects.all().delete()
    Technician.objects.all().delete()
    ServiceRecord.objects.all().delete()
    PartsUsage.objects.all().delete()
    SparePart.objects.all().delete()
    Invoice.objects.all().delete()

    print("Populating sample data...")

    # 1. Create inventory spare parts
    p1 = SparePart.objects.create(part_name='Brake Pads', quantity=25, price=45.00, supplier='Brembo Parts Ltd')
    p2 = SparePart.objects.create(part_name='Engine Oil 5W-30', quantity=40, price=29.99, supplier='Castrol Distributors')
    p3 = SparePart.objects.create(part_name='Oil Filter', quantity=9, price=12.50, supplier='Bosch Auto Parts') # Low stock (quantity <= 10)
    p4 = SparePart.objects.create(part_name='Air Filter', quantity=15, price=18.00, supplier='Mann Filters')

    # 2. Create customer users & profiles
    u_cust1 = User.objects.create_user(username='customer1', email='john@gmail.com', password='password123', role='customer', first_name='John', last_name='Doe', phone='555-0101', address='123 Maple St, Springfield')
    cust1 = Customer.objects.create(user=u_cust1, customer_name='John Doe', phone='555-0101', email='john@gmail.com', address='123 Maple St, Springfield')

    u_cust2 = User.objects.create_user(username='customer2', email='sarah@gmail.com', password='password123', role='customer', first_name='Sarah', last_name='Connor', phone='555-0202', address='742 Evergreen Terr, Springfield')
    cust2 = Customer.objects.create(user=u_cust2, customer_name='Sarah Connor', phone='555-0202', email='sarah@gmail.com', address='742 Evergreen Terr, Springfield')

    # 3. Create technician users & profiles
    u_tech1 = User.objects.create_user(username='tech1', email='bob@autoserv.com', password='password123', role='technician', first_name='Bob', last_name='Builder', phone='555-9001')
    tech1 = Technician.objects.create(user=u_tech1, name='Bob Builder', specialization='Engine tuning', phone='555-9001', experience=8)

    u_tech2 = User.objects.create_user(username='tech2', email='alice@autoserv.com', password='password123', role='technician', first_name='Alice', last_name='Smith', phone='555-9002')
    tech2 = Technician.objects.create(user=u_tech2, name='Alice Smith', specialization='Electrical diagnostics', phone='555-9002', experience=5)

    # 4. Create Service Advisor user
    User.objects.create_user(
        username='advisor1',
        email='advisor@autoserv.com',
        password='password123',
        role='service_advisor',
        first_name='Emma',
        last_name='Watson',
        phone='555-8001',
        is_staff=True
    )

    # 4. Create vehicles
    v1 = Vehicle.objects.create(customer=cust1, vehicle_number='MH12AA1234', brand='Tesla', model='Model S', year=2021, fuel_type='electric')
    v2 = Vehicle.objects.create(customer=cust1, vehicle_number='MH12BB5678', brand='Honda', model='Civic', year=2018, fuel_type='petrol')
    v3 = Vehicle.objects.create(customer=cust2, vehicle_number='MH12CC9012', brand='Toyota', model='Rav4', year=2020, fuel_type='hybrid')

    # 5. Create appointments
    # timezone.now() has timezone settings, since USE_TZ=True
    a1 = Appointment.objects.create(customer=cust1, vehicle=v2, appointment_date=timezone.now() - datetime.timedelta(days=1), service_type='oil_change', status='completed', notes='Regular oil and filter change.')
    a2 = Appointment.objects.create(customer=cust2, vehicle=v3, appointment_date=timezone.now() + datetime.timedelta(days=2), service_type='general', status='pending', notes='Check active vibration noise.')
    a3 = Appointment.objects.create(customer=cust1, vehicle=v1, appointment_date=timezone.now() - datetime.timedelta(hours=2), service_type='brakes', status='in_progress', notes='Brakes screeching.')

    # 6. Create service records & parts usage
    # Completed service
    s1 = ServiceRecord.objects.create(vehicle=v2, technician=tech1, service_date=datetime.date.today() - datetime.timedelta(days=1), description='Completed standard oil and filter replacement. Tested engine compression.', status='completed')
    PartsUsage.objects.create(service_record=s1, spare_part=p2, quantity_used=1)
    PartsUsage.objects.create(service_record=s1, spare_part=p3, quantity_used=1)
    p2.quantity -= 1; p2.save()
    p3.quantity -= 1; p3.save()

    # Ongoing service
    s2 = ServiceRecord.objects.create(vehicle=v1, technician=tech2, service_date=datetime.date.today(), description='Inspecting brake caliper wear and noise. Front brake pad replacement underway.', status='ongoing')
    PartsUsage.objects.create(service_record=s2, spare_part=p1, quantity_used=2)
    p1.quantity -= 2; p1.save()

    # 7. Create invoices
    Invoice.objects.create(service_record=s1, service_charges=50.00, parts_charges=42.49, total_amount=92.49, payment_status='paid', invoice_date=datetime.date.today())

    print("Sample data populated successfully!")

if __name__ == '__main__':
    populate()
