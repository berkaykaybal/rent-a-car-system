from django import forms
from django.contrib.auth.models import User
from .models import Vehicle, Insurance, Reservation, Payment
from accounts.models import Customer
from django.utils import timezone 

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = ['brand', 'model', 'vehicle_type', 'daily_rate', 'image', 'status']
        widgets = {
            'brand': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Brand'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Model'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type (e.g. SUV)'}),
            'daily_rate': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Daily Rate'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class InsuranceForm(forms.ModelForm):
    class Meta:
        model = Insurance
        fields = ['insurance_type', 'coverage_details', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'insurance_type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Insurance Type'}),
            'coverage_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Coverage Details'}),
        }

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['license_number', 'age']
        widgets = {
             'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'}),
             'license_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'License Number'}),
        }

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date', 'branch']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'branch': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")

        if start and end:
            if start < timezone.now().date():
                raise forms.ValidationError("Geçmiş bir tarihe rezervasyon yapılamaz.")
            if end < start:
                raise forms.ValidationError("Bitiş tarihi başlangıç tarihinden önce olamaz.")
        return cleaned_data

class PaymentForm(forms.ModelForm):
    card_number = forms.CharField(
        max_length=19, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '0000 0000 0000 0000'})
    )
    expiry_date = forms.CharField(
        max_length=5, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=3, 
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CVV'})
    )

    class Meta:
        model = Payment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control', 'id': 'id_payment_method'})
        }