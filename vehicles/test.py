from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date, timedelta
from vehicles.models import Vehicle, Reservation
from accounts.models import Customer 

class Sprint3_MainUseCaseTests(TestCase):
    

    def setUp(self):
        self.vehicle = Vehicle.objects.create(
            brand="Tesla",
            model="Model Y",
            vehicle_type="Electric",
            daily_rate=3000,
            status='Available'
        )
        self.user = User.objects.create_user(
            username='test_user', 
            password='123',
            first_name='Can',  
        )

    def test_step_1_vehicle_inventory_display(self):
        
        url = reverse('vehicle_list') 
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        
      
        self.assertContains(response, "Rent A Car") 

    def test_step_2_guest_driver_information(self):
        
        driver = Customer.objects.create(
            user=self.user,
            phone="5551234567",
            license_number="B-123456", 
            age=26                     
        )
        
        saved_driver = Customer.objects.get(license_number="B-123456")
        
        self.assertEqual(saved_driver.user.first_name, "Can") 
        self.assertEqual(saved_driver.age, 26)

    def test_step_3_reservation_core_logic(self):
       
        customer = Customer.objects.create(
            user=self.user, 
            phone="5559998877",
            age=26
        )
        
        start_date = date.today()
        end_date = date.today() + timedelta(days=3)
    
        days = (end_date - start_date).days
        expected_price = days * self.vehicle.daily_rate 
        
        
        reservation = Reservation.objects.create(
            vehicle=self.vehicle,
            customer=customer,
            start_date=start_date,
            end_date=end_date,
            branch='City Center'
        )

        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(reservation.total_price, 9000) 
        self.assertEqual(reservation.vehicle.brand, "Tesla")