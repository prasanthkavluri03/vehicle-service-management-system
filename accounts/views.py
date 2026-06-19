from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm
from customers.models import Customer

# Custom login view utilizing standard template
class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)


# User registration view
def register(request):
    if request.user.is_authenticated:
        return redirect('accounts:login_redirect')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Automatically create a linked profile depending on the selected role
            if user.role == 'customer':
                Customer.objects.create(
                    user=user,
                    customer_name=f"{user.first_name} {user.last_name}",
                    phone=user.phone or '',
                    email=user.email or '',
                    address=user.address or ''
                )
            elif user.role == 'technician':
                from technicians.models import Technician
                Technician.objects.create(
                    user=user,
                    name=f"{user.first_name} {user.last_name}",
                    specialization="General Diagnostics",
                    phone=user.phone or '',
                    experience=1
                )
            elif user.role == 'admin':
                user.is_staff = True
                user.is_superuser = True
                user.save()
            elif user.role == 'service_advisor':
                user.is_staff = True
                user.save()
                
            messages.success(request, "Registration successful! You can now log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})


# User logout view
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')


# Role-based redirection after login
@login_required
def login_redirect(request):
    role = request.user.role
    if role == 'admin' or role == 'service_advisor' or request.user.is_superuser:
        return redirect('dashboard:index')
    elif role == 'technician':
        return redirect('technicians:technician_dashboard')
    else:
        return redirect('customers:customer_dashboard')


# Profile details and editing view
@login_required
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            
            # Sync with Customer/Technician profiles if they exist
            if user.role == 'customer':
                try:
                    customer = user.customer
                    customer.customer_name = f"{user.first_name} {user.last_name}"
                    customer.phone = user.phone or ''
                    customer.email = user.email or ''
                    customer.address = user.address or ''
                    customer.save()
                except Customer.DoesNotExist:
                    pass
            elif user.role == 'technician':
                try:
                    tech = user.technician
                    tech.name = f"{user.first_name} {user.last_name}"
                    tech.phone = user.phone or ''
                    tech.save()
                except Exception:
                    pass
                    
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'accounts/profile.html', {'form': form})
