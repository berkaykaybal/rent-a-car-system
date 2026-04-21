from django.db import models
from django.utils import timezone
from accounts.models import Customer 

class Vehicle(models.Model):
    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    vehicle_type = models.CharField(max_length=50)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Available')
    image = models.ImageField(upload_to='vehicles/', blank=True, null=True)

    FUEL_CHOICES = [
        ('Gasoline', 'Gasoline'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
    ]
    fuel_type = models.CharField(max_length=20, choices=FUEL_CHOICES, default='Gasoline', verbose_name="Fuel Type")

    TRANSMISSION_CHOICES = [
        ('Automatic', 'Automatic'),
        ('Manual', 'Manual'),
    ]
    transmission = models.CharField(max_length=20, choices=TRANSMISSION_CHOICES, default='Automatic', verbose_name="Transmission")

    seats = models.IntegerField(default=5, verbose_name="Seat Count")
    luggage = models.IntegerField(default=3, verbose_name="Luggage Capacity")

    def __str__(self):
        return f"{self.brand} {self.model}"

class Insurance(models.Model):
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE, related_name='insurance')
    insurance_type = models.CharField(max_length=100)
    coverage_details = models.TextField()
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.insurance_type} - {self.vehicle.brand}"

class Reservation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reservations')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='reservations')
    start_date = models.DateField()
    end_date = models.DateField()
    
    BRANCH_CHOICES = [
        ('City Center', 'City Center'),
        ('Airport', 'Airport'),
        ('Bus Station', 'Bus Station'),
    ]
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, default='City Center')

    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending Payment', choices=[
        ('Pending Payment', 'Pending Payment'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    # Diyagramdaki calculation isteklerini karsilayan metodlar
    def calculate_duration(self):
        delta = self.end_date - self.start_date
        return delta.days if delta.days > 0 else 1

    def calculate_total_cost(self):
        duration = self.calculate_duration()
        return duration * self.vehicle.daily_rate

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            self.total_price = self.calculate_total_cost()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Res: {self.vehicle.brand} - {self.customer.user.username}"

# --- SPRINT 3: YENI EKLENEN MODEL ---
class Payment(models.Model):
    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='payment')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=[('Credit Card', 'Credit Card'), ('Cash', 'Cash')])
    penalty = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_date = models.DateTimeField(default=timezone.now)

    def process_payment(self):
        # Buraya ileride sanal pos entegrasyonu gelebilir
        return True

    def __str__(self):
        return f"Payment for Res {self.reservation.id} - {self.total_amount}"