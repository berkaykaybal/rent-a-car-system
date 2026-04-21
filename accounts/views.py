from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Customer
from .forms import CustomerRegistrationForm, CustomerProfileForm

def register_view(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            Customer.objects.create(user=user)
            login(request, user)
            
            messages.info(request, "Account created. Please complete your profile.")
            return redirect('verify_profile')
    else:
        form = CustomerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def verify_profile_view(request):
    try:
        customer = request.user.customer
    except:
        return redirect('register')

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            age = form.cleaned_data['age']
            if age is not None and age >= 18:
                form.save()
                messages.success(request, "Profile verified! You can now rent vehicles.")
                return redirect('vehicle_list')
            else:
                messages.error(request, "Sorry, you must be over 18 to rent a vehicle.")
    else:
        form = CustomerProfileForm(instance=customer)
        
    return render(request, 'accounts/verify_profile.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('vehicle_list')
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('vehicle_list')
    return redirect('vehicle_list')

def user_logout(request):
    logout(request)
    messages.info(request, "Successfully logged out. See you soon!")
    return redirect('vehicle_list')