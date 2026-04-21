from django.urls import path
from . import views

urlpatterns = [
    # Ana Sayfa ve Listeleme
    path('', views.vehicle_list, name='vehicle_list'),
    
    # Araç Ekleme ve Kayıt İşlemleri (Views dosyanla uyumlu olması için)
    path('add-vehicle/', views.add_vehicle_with_insurance, name='add_vehicle'),
    path('register/', views.register_customer, name='register'),
    path('verify-profile/', views.verify_profile, name='verify_profile'),

    # Rezervasyon (Sprint 2)
    path('reserve/<int:vehicle_id>/', views.create_reservation, name='create_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),

    # --- SPRINT 3: ÖDEME SİSTEMİ (Yeni Eklenenler) ---
    # Bu satırlar olmazsa ödeme sayfaları açılmaz!
    path('payment/<int:reservation_id>/', views.payment_summary, name='payment_summary'),
    path('payment/success/', views.payment_success, name='payment_success'),
]