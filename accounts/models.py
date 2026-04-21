from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    license_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="License Number")
    age = models.IntegerField(blank=True, null=True, verbose_name="Age")

    def __str__(self):
        return self.user.username