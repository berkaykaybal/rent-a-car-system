from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Vehicle, Insurance, Reservation, Payment
from accounts.models import Customer
from .forms import VehicleForm, InsuranceForm, UserRegistrationForm, CustomerProfileForm, ReservationForm, PaymentForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def vehicle_list(request):
    vehicles = None
    show_results = False
    
    if request.GET.get('location'): 
        vehicles = Vehicle.objects.filter(status='Available')
        pickup_date = request.GET.get('pickup_date')
        
        if pickup_date:
            reserved_vehicle_ids = Reservation.objects.filter(
                start_date__lte=pickup_date, 
                end_date__gte=pickup_date,   
                status__in=['Confirmed', 'Pending Payment'] 
            ).values_list('vehicle_id', flat=True)
            
            vehicles = vehicles.exclude(id__in=reserved_vehicle_ids)
            
        show_results = True
    
    context = {
        'vehicles': vehicles,
        'show_results': show_results,
    }
    return render(request, 'vehicles/vehicle_list.html', context)

def add_vehicle_with_insurance(request):
    if request.method == 'POST':
        v_form = VehicleForm(request.POST, request.FILES)
        i_form = InsuranceForm(request.POST)
        if v_form.is_valid() and i_form.is_valid():
            vehicle = v_form.save()
            insurance = i_form.save(commit=False)
            insurance.vehicle = vehicle
            insurance.save()
            messages.success(request, 'Vehicle added successfully!')
            return redirect('vehicle_list')
    else:
        v_form = VehicleForm()
        i_form = InsuranceForm()
    
    return render(request, 'vehicles/add_vehicle.html', {'v_form': v_form, 'i_form': i_form})

def register_customer(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            Customer.objects.create(user=user, phone=form.cleaned_data['phone'])
            login(request, user)
            return redirect('verify_profile')
    else:
        form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})

def verify_profile(request):
    try:
        customer = request.user.customer
    except AttributeError:
        return redirect('vehicle_list')

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=customer)
        if form.is_valid():
            if form.cleaned_data['age'] >= 18:
                form.save()
                return redirect('vehicle_list')
            else:
                messages.error(request, 'You must be at least 18 years old.')
    else:
        form = CustomerProfileForm(instance=customer)
    return render(request, 'vehicles/verify_profile.html', {'form': form})

@login_required
def create_reservation(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            overlapping_reservations = Reservation.objects.filter(
                vehicle=vehicle,
                start_date__lte=end_date,
                end_date__gte=start_date,
                status__in=['Confirmed', 'Pending Payment'] 
            ).exists()
            
            if overlapping_reservations:
                messages.error(request, "Unfortunately, this vehicle is already booked for the selected dates.")
            else:
                reservation = form.save(commit=False)
                reservation.vehicle = vehicle
                reservation.customer = request.user.customer
                reservation.status = 'Pending Payment'
                reservation.save()
                
                messages.success(request, "Reservation created! Please complete your payment.")
                return redirect('payment_summary', reservation_id=reservation.id)
    else:
        form = ReservationForm()

    return render(request, 'vehicles/reservation_form.html', {'form': form, 'vehicle': vehicle})

@login_required
def payment_summary(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, customer__user=request.user)
    
    if hasattr(reservation, 'payment'):
        return redirect('payment_success')
        
    duration = reservation.calculate_duration()
    total_cost = reservation.calculate_total_cost()
    
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.reservation = reservation
            payment.total_amount = total_cost
            payment.save()
            
            reservation.status = 'Confirmed'
            reservation.save()
            
            messages.success(request, "Payment successful! Your rental is confirmed.")
            return redirect('payment_success')
    else:
        form = PaymentForm()

    context = {
        'reservation': reservation,
        'duration': duration,
        'total_cost': total_cost,
        'form': form
    }
    return render(request, 'vehicles/payment_summary.html', context)

@login_required
def payment_success(request):
    return render(request, 'vehicles/payment_success.html')

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(customer=request.user.customer).order_by('-created_at')
    return render(request, 'vehicles/my_reservations.html', {'reservations': reservations})